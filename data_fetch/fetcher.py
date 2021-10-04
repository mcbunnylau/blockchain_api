import requests
from decouple import config
from api.models import Block, Event, SyncedProgress, Address

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


def update_block():
    syncs = SyncedProgress.objects.all()
    if syncs is not None:
        for sync in syncs:
            if sync.syncing is True:
                address = sync.contract_address.address
                block = sync.synced_block_height

                for i_block in range(block, block + 100000):
                    events = get_block_log_events(address, i_block)
                    if events is not None:
                        try:
                            # each event
                            for e in events:
                                # get or create block
                                block_ = Block.objects.get_or_create(
                                    block_height=i_block)

                                for i in e["decoded"]["params"]:
                                    if i["name"] == "from":
                                        from_address = Address.objects.get_or_create(
                                            address=i["value"])[0]
                                        print(from_address)
                                    elif i["name"] == "to":
                                        to_address = Address.objects.get_or_create(
                                            address=i["value"])[0]
                                        print(to_address)
                                    elif i["name"] == "value":
                                        value = int(i["value"])
                                        print(type(value))

                                # create new event
                                event = Event.objects.create(
                                    from_address=from_address, to_address=to_address, value=value)
                                print(event)
                                event.save()

                                # add event to block
                                block_.events.add(event)
                                block_.save()
                        except:
                            pass

                    # update synced block height
                    sync.synced_block_height = sync.synced_block_height + 1
                    sync.save()
