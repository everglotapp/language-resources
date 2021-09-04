/* eslint-disable camelcase */

exports.shorthands = undefined

exports.up = (pgm) => {
    pgm.createTable(
        { schema: "app_public", name: "words_{{ locale }}" },
        {
            id: "id",
            uuid: { type: "uuid", notNull: true, unique: true },
            word: {
                type: "text",
                collation: '"{{ locale }}-{{ country }}-x-icu"',
                notNull: true,
            },
            frequency: {
                type: "float",
                notNull: true,
                comment: "Ranges from 0 to 1 (higher is more frequent)",
            },
            length: {
                type: "integer",
                expressionGenerated: "char_length(word)",
            },
            recommended_skill_level_id: {
                type: "integer",
                references: {
                    schema: "app_public",
                    name: "language_skill_levels",
                },
                notNull: false,
            },
            created_at: {
                type: "timestamp with time zone",
                notNull: true,
                default: pgm.func("current_timestamp"),
            },
        },
        {
            comment: "@name {{ locale_full }}Words",
        }
    )
    pgm.alterTable(
        { schema: "app_public", name: "words_{{ locale }}" },
        {
            levelSecurity: "ENABLE",
        }
    )
    pgm.createPolicy(
        { schema: "app_public", name: "words_{{ locale }}" },
        "select_server",
        {
            command: "SELECT",
            role: "evg_server",
            using: `true`,
        }
    )
    pgm.sql(`GRANT SELECT ON app_public.words_{{ locale }} TO evg_server`)
}

exports.down = (pgm) => {
    pgm.sql(`REVOKE SELECT ON app_public.words_{{ locale }} FROM evg_server`)
    pgm.dropPolicy(
        { schema: "app_public", name: "words_{{ locale }}" },
        "select_server",
        {
            ifExists: false,
        }
    )
    pgm.alterTable(
        { schema: "app_public", name: "words_{{ locale }}" },
        {
            levelSecurity: "DISABLE",
        }
    )
    pgm.dropTable({ schema: "app_public", name: "words_{{ locale }}" })
}
