from database.db import Database, db_connection, current_jalali_datetime
import uuid

class SMSSender(Database):
    DEFAULT_MESSAGE = "SMS_TEXT"
    DEFAULT_MOBILE_NO = "PHONE_NUMBER"
    DEFAULT_TABLE_NAME = "DB"
    DEFAULT_SMS_TYPE = 13

    @staticmethod
    def send_alert(record, message=None, mobile_no=None):
        message = message or SMSSender.DEFAULT_MESSAGE
        mobile_no = mobile_no or SMSSender.DEFAULT_MOBILE_NO
        date_str, time_str, datetime_str = current_jalali_datetime()
        
        sms_data = {
            "Id": str(uuid.uuid4()),
            "Message": message,
            "Comment": "",
            "Param1": "",
            "Param2": "",
            "ParamCount": 0,
            "MobileNo": mobile_no,
            "MessageKey": None,
            "OldMessageKey": None,
            "InSending": False,
            "CreateDateTime": datetime_str,
            "HasExpaired": False,
            "IsSuccessful": False,
            "EntityUniqueInfo": record,
            "RelatedEntityId": record,
            "RelatedTableName": SMSSender.DEFAULT_TABLE_NAME,
            "Status": None,
            "ExpirationDate": date_str,
            "CheckStatusDateTime": "",
            "TemplateName": "",
            "SmsType": SMSSender.DEFAULT_SMS_TYPE,
            "RequestUserId": None,
            "IsSendToServerOutbox": False,
            "SendDateTime": datetime_str
        }

        try:
            with db_connection() as conn, conn.cursor() as cursor:
                placeholders = ", ".join(["%s"] * len(sms_data))
                columns = ", ".join(sms_data.keys())
                sql = f"INSERT INTO SmsOutbox ({columns}) VALUES ({placeholders})"
                cursor.execute(sql, tuple(sms_data.values()))
                conn.commit()
                print('+ Alert sent successfully.\n')
        except Exception as e:
            print(f"[Error] Insert failed for record {record}: {e}")