-- Drop existing telegram-related columns if they exist
-- SQLite doesn't support ALTER TABLE DROP, so we'll use pragma

-- CreateTable User (fresh)
-- Since SQLite has limitations, we'll recreate the table structure
PRAGMA foreign_keys=OFF;

CREATE TABLE "User_new" (
    "id" TEXT NOT NULL PRIMARY KEY,
    "email" TEXT UNIQUE,
    "name" TEXT,
    "phone" TEXT,
    "authToken" TEXT UNIQUE,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);

INSERT INTO "User_new" ("id", "email", "name", "phone", "createdAt", "updatedAt")
SELECT "id", "email", "name", "phone", "createdAt", "updatedAt" FROM "User";

DROP TABLE "User";
ALTER TABLE "User_new" RENAME TO "User";

PRAGMA foreign_keys=ON;
