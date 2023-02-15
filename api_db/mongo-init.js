db.createUser(
    {
        user: 'admin',
        pwd: 'SuperSecret',
        roles: [
            {
                role: 'readWrite',
                db: 'api'
            },
            {
                role: 'readWrite',
                db: 'admin'
            }
        ],
    }
);

db.auth('admin', 'SuperSecret')

db = db.getSiblingDB('api')

db.createCollection('controllers');
db.createCollection('darpal');