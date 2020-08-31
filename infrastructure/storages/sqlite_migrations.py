import aiosqlite
from abstractions.recognition_settings import RecognitionSettings

settings = RecognitionSettings()

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
''',
'''
    create table if not exists "Distance" (
        "feature_id_from" text not null,
        "feature_id_to" text not null,
        "user_id_from" text not null,
        "user_id_to" text not null,
        "created_at" text not null,
        "updated_at" text nll,
        foreign key ("feature_id_from") REFERENCES "Feature" ("feature_id"),
        foreign key ("feature_id_to") REFERENCES "Feature" ("feature_id"),
        foreign key ("user_id_from") REFERENCES "User" ("user_id"),
        foreign key ("user_id_to") REFERENCES "User" ("user_id")
        on delete cascade
        on update no action
    );
'''
,
'''
    create table if not exists "RecognitionSetting" (
        "name" text primary key,
        "is_active" integer not null,
        "max_features" integer not null,
        "base_threshold" real not null,
        "rate_of_decreasing_threshold_with_each_feature" real not null,
        "created_at" text not null,
        "updated_at" text,
        "resize_factors_x" real not null,
        "resize_factors_y" real not null
    )
''',
f'''
    insert or ignore into "RecognitionSetting" (
        "name",
        "is_active",
        "max_features",
        "base_threshold",
        "rate_of_decreasing_threshold_with_each_feature",
        "created_at",
        "updated_at",
        "resize_factors_x",
        "resize_factors_y"
    ) values (
        "{settings.name}",
        1,
        {settings.max_features},
        {settings.base_threshold},
        {settings.rate_of_decreasing_threshold_with_each_feature},
        "{str(settings.created_at)}",
        null,
        {settings.resize_factors.x},
        {settings.resize_factors.y}
    )
'''
]
