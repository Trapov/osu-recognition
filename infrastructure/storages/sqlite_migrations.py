import aiosqlite

migration_scripts = [
'''
    create table if not exists "User" (
        "user_id" text primary key,
        "created_at" text not null
    );
''',
'''
    create table if not exists "Grant" (
        "user_id" text,
        "grant" text not null,
        "created_at" text not null,
        primary key ("user_id", "grant"),
        foreign key ("user_id")
        REFERENCES "User" ("user_id")
        on delete cascade
        on update no action
    );
''',
'''
    create table if not exists "Feature" (
        "feature_id" text primary key,
        "user_id" text not null,
        "image_type" text not null,
        "feature" BLOB not null,
        "created_at" text not null,
        foreign key ("user_id")
        REFERENCES "User" ("user_id")
        on delete cascade
        on update no action
    );
'''
]
