import requests
from decouple import config
from api.models import Block, LogEvent, SyncedProgress, Address

# return list of events


def get_block_log_events(address, block):
    s_block = block
    e_block = s_block + 1
    url = "https://api.covalenthq.com/v1/1/events/address/" + address + "/?starting-block=" + \
        str(s_block) + "&ending-block=" + str(e_block) + \
        "&key=" + config("COVALENT_KEY") + ""

    r = requests.get(url)

    try:
        r.raise_for_status()
        events = r.json()["data"]["items"]
        return events
    except:
        return None


def add_events_to_block(current_height, events):
    for event_ in events:
        # pulling from, to, value from params list
        # from_address = "", to_address = "", value = 0
        for i in event_["decoded"]["params"]:
            print("i = " + str(i))
            if i["name"] == "from":
                from_address = Address.objects.get_or_create(
                    address=i["value"])[0]
                from_address.save()
            elif i["name"] == "to":
                to_address = Address.objects.get_or_create(
                    address=i["value"])[0]
                to_address.save()
            elif i["name"] == "value":
                value = int(i["value"])

        # creating new event object
        try:
            print(from_address)
            print(to_address)
            print(value)
            block = Block.objects.get_or_create(
                block_height=current_height)[0]
            event = LogEvent(
                from_address=from_address,
                to_address=to_address,
                value=value)
            print("created event")
            event.save()
            block.events.add(event)
            block.save()
        except:
            print("cannot create event")


def sync_contract(contract, latest_height):
    current_height = contract.synced_block_height
    # (latest_height - 1) so covalent api end block doesn't break...
    while current_height < (latest_height - 1):
        print(current_height)  # debug
        events = get_block_log_events(
            contract.contract_address.address, current_height)
        if events is not None:
            try:
                add_events_to_block(current_height, events)
            except:
                pass

        # update SyncProgress contract object
        current_height += 1
        contract.synced_block_height = current_height
        contract.save()


def daily_sync():
    # latest_height = requests.get(
    #     "https://api.blockcypher.com/v1/eth/main").json()["height"]
    latest_height = 13000050
    print(latest_height)
    for contract in SyncedProgress.objects.all():
        print(contract)
        if contract.syncing == True:
            sync_contract(contract, latest_height)
