import os
from flask import Flask, request, redirect, abort
from models import init_db, LinkToken, LinkClick

DB_URL = os.getenv("DB_URL", "sqlite:////app/data/family_bot.db")
Session = init_db(DB_URL)

app = Flask(__name__)

TARGETS = {
    "register": "https://livegoodtour.com/Aymanbenz",
    "company_video": "https://youtu.be/BmkpPgppwI4?si=7zu-jR_3ySE5wYI2",
    "earnings_video": "https://youtu.be/zcCHub9Schg?si=V2-TRzxhrKnSaLSk"
}

@app.route("/r/<token>")
def track_redirect(token):
    session = Session()
    lt = session.query(LinkToken).filter_by(token=token).first()
    if not lt:
        session.close()
        abort(404)

    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ua = request.headers.get("User-Agent")

    click = LinkClick(
        token=token,
        tg_id=lt.tg_id,
        link_key=lt.link_key,
        ip=ip,
        user_agent=ua
    )
    session.add(click)
    session.commit()
    session.close()

    target = TARGETS.get(lt.link_key)
    if not target:
        abort(404)

    return redirect(target, code=302)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
