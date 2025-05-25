import os, json, logging, requests
import azure.functions as func

SECRET = os.getenv("CHAT_TOKEN")
ORIGIN = os.getenv("STATIC_ORIGIN")

def main(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return func.HttpResponse(status_code=204, headers={
            "Access-Control-Allow-Origin": ORIGIN,
            "Access-Control-Allow-Methods": "POST,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type,X-Chat-Token"
        })
    token = req.headers.get("X-Chat-Token")
    if token != SECRET:
        return func.HttpResponse("Unauthorized", status_code=401,
                                 headers={"Access-Control-Allow-Origin":ORIGIN})
    try:
        data = req.get_json()
        user_msg = data.get("message","")
        # Call an n8n or AI here:
        resp = requests.post(os.getenv("N8N_WEBHOOK_URL"),
                             json={"message":user_msg}, timeout=10)
        reply = resp.json().get("reply","")
        return func.HttpResponse(
          json.dumps({"reply":reply}),
          status_code=200,
          mimetype="application/json",
          headers={"Access-Control-Allow-Origin":ORIGIN}
        )
    except Exception as e:
        logging.exception(e)
        return func.HttpResponse("Server error", status_code=500,
                                 headers={"Access-Control-Allow-Origin":ORIGIN})
