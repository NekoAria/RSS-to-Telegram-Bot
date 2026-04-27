#  RSS to Telegram Bot
#  Copyright (C) 2026  Rongrong <i@rong.moe>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "cache" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "entry_hash" VARCHAR(8) NOT NULL,
    "feed_id" INT NOT NULL REFERENCES "feed" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_cache_feed_id_dfdbbf" UNIQUE ("feed_id", "entry_hash")
);
        COMMENT ON COLUMN "cache"."created_at" IS 'The time this row was created';
        COMMENT ON COLUMN "cache"."updated_at" IS 'The time this row was updated';
        COMMENT ON COLUMN "cache"."entry_hash" IS 'Hash (CRC32) of entry';
        COMMENT ON TABLE "cache" IS 'Cache model.';
        INSERT INTO "cache" ("feed_id", "entry_hash")
        SELECT "feed"."id", elem
        FROM "feed", jsonb_array_elements_text("feed"."entry_hashes"::jsonb) AS elem
        WHERE "feed"."entry_hashes" IS NOT NULL;
        ALTER TABLE "feed" DROP COLUMN "entry_hashes";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "feed" ADD "entry_hashes" TEXT;
        COMMENT ON COLUMN "feed"."entry_hashes" IS 'Hashes (CRC32) of entries';
        DROP TABLE IF EXISTS "cache";"""
