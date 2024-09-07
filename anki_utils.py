import requests


def anki_request(action, params={}):
    request_json = {
        "action": action,
        "version": 6,
        "params": params
    }
    response = requests.post('http://localhost:8765', json=request_json).json()

    if response.get('error'):
        raise Exception(f"AnkiConnect error: {response['error']}")
    return response['result']


def manual_control(deck_name, front_text, back_text, tags=["auto_generated"]):
    print(f"Trying to add the following card to deck {deck_name}")
    print(f"\033[1mFront: \033[0m{
          front_text}\n\033[1mBack: \033[0m{back_text}")
    response = input("Include? [(y)es/(n)o/(m)odify]: ")

    if response.lower().strip() in ["yes", "y", ""]:
        add_card(deck_name, front_text, back_text, tags)
    elif response.lower().strip() in ["mod", "modify", "m"]:
        modify_option = input(
            "Modify (f)ront, (b)ack, or b(o)th?: ").lower().strip()

        if modify_option in ["f", "front"]:
            front_text = input("Enter new front text: ").strip()
        elif modify_option in ["b", "back"]:
            back_text = input("Enter new back text: ").strip()
        elif modify_option in ["o", "both"]:
            front_text = input("Enter new front text: ").strip()
            back_text = input("Enter new back text: ").strip()

        print(f"Updated card:\n\033[1mFront: \033[0m{
              front_text}\n\033[1mBack: \033[0m{back_text}")
        final_decision = input("Include this card? [(y)es/(n)o]: ")

        if final_decision.lower().strip() in ["yes", "y", ""]:
            add_card(deck_name, front_text, back_text, tags)
    else:
        print("Card not added.")


def add_card(deck_name, front_text, back_text, tags=["auto_generated"]):
    note = {
        "deckName": deck_name,             # Specify the deck name
        "modelName": "Basic",              # Card type (e.g., "Basic", "Cloze")
        "fields": {                        # Fields for the note (front and back)
            "Front": front_text,
            "Back": back_text
        },
        "tags": tags                       # Optional tags
    }

    # Send the request to add the note
    anki_request('addNotes', {"notes": [note]})


def create_deck(deck_name):
    anki_request('createDeck', {"deck": deck_name})


if __name__ == "__main__":
    front_text = input("Front text: ")
    back_text = input("Back text: ")
    manual_control("Test 1 2 3", front_text, back_text)
