from producer import TwitterProducer
import os

# with open(f"{os.path.abspath(os.getcwd())}/kafka/twitter_producer/secret", "r") as file:
#     bearer_token = file.readline().split(' ')[2].split('\n')[0]

api_key = "MuRAjvVic6MpFNLPGJK7o67hy"
api_key_secret = "YITaLPgOQwC5mX6GKstCeNhzWUaEoRIh1a8DpKzltef5ja9qkz"
access_token = "1734205566950735872-SvTXJ68oHWA22mXFuL4WTY0x13vA6J"
token_secret = "UYUIxTY4W3EHcyCxoDUoaWXcKimqQ68a3pKiAxQI2Y0XQ"

bearer_token = "AAAAAAAAAAAAAAAAAAAAADTHrQEAAAAA6%2F%2FEi3lvtGGgjMX2mH1kCPIpfYc%3Dc1jWfKMYFPuoSj9bCoFMEe072rmUH5BwLjdChXif3sQ1oztEuL"
def run_service():
    producer = TwitterProducer(bearer_token = token_secret, return_type=dict)
    print(f"After create producer")
    producer.run()




if __name__ == "__main__":
    print("------Start----- ")
    run_service()