import os
from pathlib import Path
from databases.database import db
from server.app import app

# main activities
if __name__ == "__main__":
    if not os.path.exists("databases"):
        os.mkdir("databases")

    filePath = Path("databases" + os.sep + "beresta_data.db")
    filePath.touch(exist_ok=True)

    db.recreate_table()

    app.run(debug=True, port=12289)
