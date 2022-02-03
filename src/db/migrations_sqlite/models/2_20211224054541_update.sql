-- upgrade --
CREATE TABLE IF NOT EXISTS "cache" (
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* The time this row was created */,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* The time this row was updated */,
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "entry_hash" VARCHAR(8)   /* Hash (CRC32) of entry */,
    "feed_id" INT NOT NULL REFERENCES "feed" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_cache_feed_id_dfdbbf" UNIQUE ("feed_id", "entry_hash")
) /* Cache model. */;;
-- ALTER TABLE "feed" DROP COLUMN "entry_hashes";
-- downgrade --
-- ALTER TABLE "feed" ADD "entry_hashes" TEXT   /* Hashes (CRC32) of entries */;
DROP TABLE IF EXISTS "cache";
