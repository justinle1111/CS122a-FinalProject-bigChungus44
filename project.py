import sys
from services.import_data import import_data
from services.insert_agent_client import insertAgentClient
from services.add_customized_model import addCustomizedModel
from services.delete_base_model import deleteBaseModel
from services.list_internet_service import listInternetService
from services.count_customized_model import countCustomizedModel
from services.top_n_duration_config import topNDurationConfig
from services.list_base_model_keyword import listBaseModelKeyword


def main():
    if len(sys.argv) < 2:
        print("Fail")
        return

    command = sys.argv[1]

    # ------------------------------
    # 1. IMPORT DATA
    # ------------------------------
    if command == "import":
        if len(sys.argv) != 3:
            print("Fail")
            return
        result = import_data(sys.argv[2])
        print("Success" if result else "Fail")
        return

    # ------------------------------
    # 2. INSERT AGENT CLIENT
    # python3 project.py insertAgentClient uid username email card_number card_holder expiration cvv zip interests
    # ------------------------------
    if command == "insertAgentClient":
        if len(sys.argv) != 11:
            print("Fail")
            return
        
        uid = sys.argv[2]
        username = sys.argv[3]
        email = sys.argv[4]
        card_number = sys.argv[5]
        card_holder = sys.argv[6]
        expiration_date = sys.argv[7]
        cvv = sys.argv[8]
        zip_code = sys.argv[9]
        interests = sys.argv[10]

        result = insertAgentClient(uid, username, email, card_number,
                                   card_holder, expiration_date, cvv,
                                   zip_code, interests)
        print("Success" if result else "Fail")
        return

    # ------------------------------
    # 3. ADD CUSTOMIZED MODEL
    # python3 project.py addCustomizedModel mid bmid
    # ------------------------------
    if command == "addCustomizedModel":
        if len(sys.argv) != 4:
            print("Fail")
            return

        mid = sys.argv[2]
        bmid = sys.argv[3]

        result = addCustomizedModel(mid, bmid)
        print("Success" if result else "Fail")
        return

    # ------------------------------
    # 4. DELETE BASE MODEL
    # python3 project.py deleteBaseModel bmid
    # ------------------------------
    if command == "deleteBaseModel":
        if len(sys.argv) != 4:
            print("Fail")
            return

        bmid = sys.argv[2]
        result = deleteBaseModel(bmid)
        print("Success" if result else "Fail")
        return

    # ------------------------------
    # 5. LIST INTERNET SERVICE
    # python3 project.py listInternetService bmid
    # ------------------------------
    if command == "listInternetService":
        if len(sys.argv) != 3:
            print("Fail")
            return

        bmid = sys.argv[2]
        result = listInternetService(bmid)
        print("Success" if result else "Fail")
        return

    # ------------------------------
    # 6. COUNT CUSTOMIZED MODEL
    # python3 project.py countCustomizedModel bmid1 bmid2 bmid3 ...
    # ------------------------------
    if command == "countCustomizedModel":
        if len(sys.argv) < 3:
            print("Fail")
            return

        bmid_list = sys.argv[2:]
        result = countCustomizedModel(bmid_list)
        print("Success" if result else "Fail")
        return

    # ------------------------------
    # 7. TOP N DURATION CONFIG
    # python3 project.py topNDurationConfig uid N
    # ------------------------------
    if command == "topNDurationConfig":
        if len(sys.argv) != 4:
            print("Fail")
            return

        uid = sys.argv[2]
        N = sys.argv[3]
        result = topNDurationConfig(uid, N)
        print("Success" if result else "Fail")
        return

    # ------------------------------
    # 8. LIST BASE MODEL KEYWORD
    # python3 project.py listBaseModelKeyword keyword
    # ------------------------------
    if command == "listBaseModelKeyWord":
        if len(sys.argv) != 3:
            print("Fail")
            return

        keyword = sys.argv[2]
        result = listBaseModelKeyword(keyword)
        print("Success" if result else "Fail")
        return

    # ------------------------------
    # INVALID COMMAND
    # ------------------------------
    print("Fail")


if __name__ == "__main__":
    main()
