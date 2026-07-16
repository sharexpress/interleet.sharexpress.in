# Copyright 2026 Sharexpress Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import json
from app.core.db import get_db

async def main():
    db = get_db()
    # Get one frontend challenge in full detail
    p = await db.problems.find_one({"slug": "toast-queue-manager"})
    if p:
        p.pop("_id", None)
        print(json.dumps(p, indent=2, default=str))
    
    print("\n\n=== TEST CASES ===")
    cursor = db.test_cases.find({"problem_slug": "toast-queue-manager"})
    async for tc in cursor:
        tc.pop("_id", None)
        print(json.dumps(tc, indent=2, default=str))

asyncio.run(main())
