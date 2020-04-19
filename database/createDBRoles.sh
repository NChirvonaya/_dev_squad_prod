mongo ${MONGODBNAME} --port 28000 -u $MONGOADMINUSER -p $MONGOADMINPASS --authenticationDatabase admin <<EOF
    db.createCollection("Users", {autoIndexId: True})
    db.createCollection("Stats", {autoIndexId: True})
    db.createCollection("Images", {autoIndexId: True})
    db.createCollection("Subscriptions", {autoIndexId: True})
    db.createCollection("SubscriptionTypes", {autoIndexId: True})
    db.createCollection("ActivityLog", {autoIndexId: True})
    db.createCollection("ActivityTypes", {autoIndexId: True})
    db.createCollection("RoleTypes", {autoIndexId: True})
    db.createRole(
        {
            role: "client",
            privileges: [
                resource: {db: "${MOGODBNAME}", collection:"Users"}, actions: ["find"],
                resource: {db: "${MOGODBNAME}", collection:"Stats"}, actions: ["find"],
                resource: {db: "${MOGODBNAME}", collection:"Images"}, actions: ["find"],
                resource: {db: "${MOGODBNAME}", collection:"Subscriptions"}, actions: ["find"],
                resource: {db: "${MOGODBNAME}", collection:"SubscriptionTypes"}, actions: ["find"],
                resource: {db: "${MOGODBNAME}", collection:"ActivityLog"}, actions: ["insert"],
                resource: {db: "${MOGODBNAME}", collection:"ActivityTypes"}, actions: ["find"],
                resource: {db: "${MOGODBNAME}", collection:"RoleTypes"}, actions: ["find"]
            ],
            roles: []
        }
    );
    db.createRole(
        {
            role: "scrapper",
            privileges: [
                resource: {db: "${MOGODBNAME}", collection:"Users"}, actions: ["find"],
                resource: {db: "${MOGODBNAME}", collection:"Stats"}, actions: ["find", "insert", "update"],
                resource: {db: "${MOGODBNAME}", collection:"Images"}, actions: ["find", "insert", "update"],
                resource: {db: "${MOGODBNAME}", collection:"Subscriptions"}, actions: ["find"],
                resource: {db: "${MOGODBNAME}", collection:"SubscriptionTypes"}, actions: ["find"],
                resource: {db: "${MOGODBNAME}", collection:"RoleTypes"}, actions: ["find"]
            ],
            roles: []
        }
    );
    db.createRole(
        {
            role: "admin",
            privileges: [
                resource: {db: "${MOGODBNAME}", collection:"Users"}, actions: ["find", "insert", "update", "remove"],
                resource: {db: "${MOGODBNAME}", collection:"Stats"}, actions: ["find", "insert", "update", "remove"],
                resource: {db: "${MOGODBNAME}", collection:"Images"}, actions: ["find", "insert", "update", "remove"],
                resource: {db: "${MOGODBNAME}", collection:"Subscriptions"}, actions: ["find", "insert", "update", "remove"],
                resource: {db: "${MOGODBNAME}", collection:"SubscriptionTypes"}, actions: ["find"],
                resource: {db: "${MOGODBNAME}", collection:"ActivityLog"}, actions: ["find", "insert"],
                resource: {db: "${MOGODBNAME}", collection:"ActivityTypes"}, actions: ["find"],
                resource: {db: "${MOGODBNAME}", collection:"RoleTypes"}, actions: ["find", "insert", "update", "remove"]
            ],
            roles: []
        }
    );
    use admin;
    db.createUser(
        {
            user: '${1}',
            pwd: '${2}',
            roles: [
                {
                    role: 'client',
                    db: '${MONGODBNAME}'
                }
            ]
        }
    )
    db.createUser(
        {
            user: 'scrapper',
            pwd: '${MONGOSCARAPPERPASS}',
            roles: [
                {
                    role: 'scrapper',
                    db: '${MONGODBNAME}'
                }
            ]
        }
    )
EOF