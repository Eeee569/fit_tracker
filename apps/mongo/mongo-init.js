db.createUser(
        {
            user: "default",
            pwd: "default1234",
            roles: [
                {
                    role: "readWrite",
                    db: "fitdb"
                }
            ]
        }
);