#!/usr/bin/env python3

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

"""
fix_frontend_tests.py
Replaces all Frontend challenge test cases with strict, behavioral tests
that require working JavaScript.
"""

import json
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["interleet"]
col = db["problems"]

FRONTEND_TESTS = {}

# ── SIMPLE CLICK COUNTER ────────────────────────────────────────────────────
FRONTEND_TESTS["simple-click-counter"] = [
    {
        "id": "cc-tc-1",
        "name": "Increment button increases count by 1 each click",
        "hidden": False,
        "weight": 1,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const incBtn=document.getElementById('increment');const countSpan=document.getElementById('count');if(!incBtn||!countSpan)return 'FAIL: missing #increment or #count';const before=parseInt(countSpan.textContent.trim(),10)||0;incBtn.click();const after=parseInt(countSpan.textContent.trim(),10);return after===before+1?'PASS':'FAIL: expected count '+(before+1)+' but got '+after;"}),
    },
    {
        "id": "cc-tc-2",
        "name": "Three clicks → counter equals 3",
        "hidden": False,
        "weight": 1,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const incBtn=document.getElementById('increment');const countSpan=document.getElementById('count');if(!incBtn||!countSpan)return 'FAIL: missing elements';for(let i=0;i<3;i++)incBtn.click();const count=parseInt(countSpan.textContent.trim(),10);return count===3?'PASS':'FAIL: expected 3, got '+count;"}),
    },
    {
        "id": "cc-tc-3",
        "name": "Reset button sets count back to 0",
        "hidden": True,
        "weight": 1,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const incBtn=document.getElementById('increment');const resetBtn=document.getElementById('reset');const countSpan=document.getElementById('count');if(!resetBtn)return 'FAIL: missing #reset button';if(!incBtn||!countSpan)return 'FAIL: missing #increment or #count';incBtn.click();incBtn.click();incBtn.click();const before=parseInt(countSpan.textContent.trim(),10);if(before!==3)return 'FAIL: expected count to be 3 before reset, got '+before;resetBtn.click();const after=parseInt(countSpan.textContent.trim(),10);return after===0?'PASS':'FAIL: expected 0 after reset, got '+after;"}),
    },
]

# ── TODO LIST APP ───────────────────────────────────────────────────────────
FRONTEND_TESTS["todo-list-app"] = [
    {
        "id": "tla-1",
        "name": "Clicking Add creates a new list item with the typed text",
        "hidden": False,
        "weight": 1,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const input=document.getElementById('todo-input');const btn=document.getElementById('add-btn');const list=document.getElementById('todo-list');if(!input||!btn||!list)return 'FAIL: missing #todo-input, #add-btn, or #todo-list';const before=list.querySelectorAll('.todo-item').length;input.value='Buy milk';btn.click();const after=list.querySelectorAll('.todo-item').length;if(after!==before+1)return 'FAIL: expected '+(before+1)+' items, got '+after;const text=list.querySelector('.todo-item')?.textContent||'';return text.includes('Buy milk')?'PASS':'FAIL: item text does not include input value';"}),
    },
    {
        "id": "tla-2",
        "name": "Empty input does not add item",
        "hidden": False,
        "weight": 1,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const input=document.getElementById('todo-input');const btn=document.getElementById('add-btn');const list=document.getElementById('todo-list');if(!input||!btn||!list)return 'FAIL: missing elements';input.value='';const before=list.querySelectorAll('.todo-item').length;btn.click();const after=list.querySelectorAll('.todo-item').length;return after===before?'PASS':'FAIL: empty input should not add items, count changed from '+before+' to '+after;"}),
    },
    {
        "id": "tla-3",
        "name": "Delete button removes item from list",
        "hidden": True,
        "weight": 2,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const input=document.getElementById('todo-input');const btn=document.getElementById('add-btn');const list=document.getElementById('todo-list');if(!input||!btn||!list)return 'FAIL: missing elements';input.value='Test Item';btn.click();const before=list.querySelectorAll('.todo-item').length;const delBtn=list.querySelector('.delete-btn');if(!delBtn)return 'FAIL: no .delete-btn found inside todo items';delBtn.click();const after=list.querySelectorAll('.todo-item').length;return after===before-1?'PASS':'FAIL: expected '+(before-1)+' items after delete, got '+after;"}),
    },
]

# ── STOPWATCH TIMER ─────────────────────────────────────────────────────────
FRONTEND_TESTS["stopwatch-timer"] = [
    {
        "id": "sw-1",
        "name": "All required UI elements exist",
        "hidden": False,
        "weight": 1,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const ids=['display','start-btn','stop-btn','lap-btn','reset-btn','lap-list'];const missing=ids.filter(id=>!document.getElementById(id));return missing.length===0?'PASS':'FAIL: missing IDs: '+missing.join(', ');"}),
    },
    {
        "id": "sw-2",
        "name": "Start button updates the display after 200ms",
        "hidden": False,
        "weight": 2,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const startBtn=document.getElementById('start-btn');const display=document.getElementById('display');if(!startBtn||!display)return 'FAIL: missing elements';const initial=display.textContent.trim();startBtn.click();return new Promise(resolve=>{setTimeout(()=>{const updated=display.textContent.trim();resolve(updated!==initial?'PASS':'FAIL: display did not change after start ('+initial+' => '+updated+')');},200);});"}),
    },
    {
        "id": "sw-3",
        "name": "Lap button appends an entry to #lap-list",
        "hidden": True,
        "weight": 2,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const startBtn=document.getElementById('start-btn');const lapBtn=document.getElementById('lap-btn');const lapList=document.getElementById('lap-list');if(!startBtn||!lapBtn||!lapList)return 'FAIL: missing elements';startBtn.click();return new Promise(resolve=>{setTimeout(()=>{const before=lapList.children.length;lapBtn.click();const after=lapList.children.length;resolve(after>before?'PASS':'FAIL: lap-list did not grow after lap click (before='+before+', after='+after+')');},150);});"}),
    },
    {
        "id": "sw-4",
        "name": "Reset button resets display to 00:00.000",
        "hidden": True,
        "weight": 2,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const startBtn=document.getElementById('start-btn');const stopBtn=document.getElementById('stop-btn');const resetBtn=document.getElementById('reset-btn');const display=document.getElementById('display');if(!startBtn||!stopBtn||!resetBtn||!display)return 'FAIL: missing elements';startBtn.click();return new Promise(resolve=>{setTimeout(()=>{stopBtn.click();resetBtn.click();const val=display.textContent.trim();const isReset=val==='00:00.000'||val==='00:00:000'||val==='00:00.00';resolve(isReset?'PASS':'FAIL: display should reset to 00:00.000, got '+val);},200);});"}),
    },
]

FRONTEND_TESTS["form-validator"] = [
    {
        "id": "fv-1",
        "name": "All form elements are present",
        "hidden": False,
        "weight": 1,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const ids=['register-form','username','email','password','confirm-password','submit-btn'];const missing=ids.filter(id=>!document.getElementById(id));return missing.length===0?'PASS':'FAIL: missing: '+missing.join(', ');"}),
    },
    {
        "id": "fv-2",
        "name": "Real-time validation enables/disables submit button correctly",
        "hidden": False,
        "weight": 2,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const username=document.getElementById('username');const email=document.getElementById('email');const password=document.getElementById('password');const confirm=document.getElementById('confirm-password');const btn=document.getElementById('submit-btn');if(!username||!email||!password||!confirm||!btn)return 'FAIL: missing required form elements';function fill(u,e,p,c){username.value=u;email.value=e;password.value=p;confirm.value=c;username.dispatchEvent(new Event('input',{bubbles:true}));email.dispatchEvent(new Event('input',{bubbles:true}));password.dispatchEvent(new Event('input',{bubbles:true}));confirm.dispatchEvent(new Event('input',{bubbles:true}));}fill('user123','test@example.com','SecurePass1','SecurePass1');if(btn.disabled)return 'FAIL: submit button should be enabled when all fields are valid';fill('user123','bad-email','SecurePass1','SecurePass1');if(!btn.disabled)return 'FAIL: submit button should be disabled for invalid email';fill('us','test@example.com','SecurePass1','SecurePass1');if(!btn.disabled)return 'FAIL: submit button should be disabled for username shorter than 3 characters';fill('user123','test@example.com','secretpass','secretpass');if(!btn.disabled)return 'FAIL: submit button should be disabled for password lacking uppercase/number';fill('user123','test@example.com','SecurePass1','SecurePass1');if(btn.disabled)return 'FAIL: submit button should re-enable when all fields are corrected to valid';return 'PASS';"}),
    },
    {
        "id": "fv-3",
        "name": "Mismatched passwords disables submit and shows error message",
        "hidden": True,
        "weight": 2,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const username=document.getElementById('username');const email=document.getElementById('email');const password=document.getElementById('password');const confirm=document.getElementById('confirm-password');const btn=document.getElementById('submit-btn');if(!username||!email||!password||!confirm||!btn)return 'FAIL: missing required form elements';function fill(u,e,p,c){username.value=u;email.value=e;password.value=p;confirm.value=c;username.dispatchEvent(new Event('input',{bubbles:true}));email.dispatchEvent(new Event('input',{bubbles:true}));password.dispatchEvent(new Event('input',{bubbles:true}));confirm.dispatchEvent(new Event('input',{bubbles:true}));}fill('user123','test@example.com','SecurePass1','DifferentPass2');if(!btn.disabled)return 'FAIL: submit button should be disabled when passwords mismatch';const els=Array.from(document.querySelectorAll('.error,.error-msg,.invalid,[data-error],span,div,p'));const hasError=els.some(el=>{const txt=el.textContent.toLowerCase();const style=window.getComputedStyle(el);return style.display!=='none'&&style.visibility!=='hidden'&&(txt.includes('match')||txt.includes('differ')||txt.includes('same')||txt.includes('password'));});if(!hasError)return 'FAIL: should display a visible error message when passwords mismatch';fill('user123','test@example.com','SecurePass1','SecurePass1');if(btn.disabled)return 'FAIL: submit button should re-enable when passwords are corrected to match';return 'PASS';"}),
    },
]

# ── MARKDOWN PREVIEW ────────────────────────────────────────────────────────
FRONTEND_TESTS["markdown-preview"] = [
    {
        "id": "mp-1",
        "name": "Editor and preview panes are present",
        "hidden": False,
        "weight": 1,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const inp=document.getElementById('md-input');const prev=document.getElementById('md-preview');return (inp&&prev)?'PASS':'FAIL: missing #md-input or #md-preview';"}),
    },
    {
        "id": "mp-2",
        "name": "Typing # Hello World renders an <h1> in preview",
        "hidden": False,
        "weight": 2,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const inp=document.getElementById('md-input');const prev=document.getElementById('md-preview');if(!inp||!prev)return 'FAIL: missing elements';inp.value='# Hello World';inp.dispatchEvent(new Event('input',{bubbles:true}));return new Promise(resolve=>{setTimeout(()=>{const hasH1=prev.querySelector('h1')!==null;const text=prev.textContent||prev.innerHTML;resolve(hasH1&&text.includes('Hello World')?'PASS':'FAIL: typing # Hello World should render an <h1> in preview. Got: '+prev.innerHTML.substring(0,200));},100);});"}),
    },
    {
        "id": "mp-3",
        "name": "Bold **text** renders <strong> in preview",
        "hidden": True,
        "weight": 2,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const inp=document.getElementById('md-input');const prev=document.getElementById('md-preview');if(!inp||!prev)return 'FAIL: missing elements';inp.value='**bold text**';inp.dispatchEvent(new Event('input',{bubbles:true}));return new Promise(resolve=>{setTimeout(()=>{const hasStrong=prev.querySelector('strong,b')!==null;resolve(hasStrong?'PASS':'FAIL: **bold text** should render <strong> in preview. Got: '+prev.innerHTML.substring(0,200));},100);});"}),
    },
]

# ── COLOR PALETTE GENERATOR ─────────────────────────────────────────────────
FRONTEND_TESTS["color-palette"] = [
    {
        "id": "cp-1",
        "name": "Generate button creates exactly 5 swatches",
        "hidden": False,
        "weight": 2,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const btn=document.getElementById('generate-btn');const palette=document.getElementById('palette');if(!btn||!palette)return 'FAIL: missing #generate-btn or #palette';btn.click();const swatches=palette.querySelectorAll('.color-swatch');return swatches.length===5?'PASS':'FAIL: expected 5 .color-swatch elements after generate, got '+swatches.length;"}),
    },
    {
        "id": "cp-2",
        "name": "Each swatch has a background color applied",
        "hidden": False,
        "weight": 2,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const btn=document.getElementById('generate-btn');const palette=document.getElementById('palette');if(!btn||!palette)return 'FAIL: missing elements';btn.click();const swatches=Array.from(palette.querySelectorAll('.color-swatch'));if(swatches.length===0)return 'FAIL: no swatches found';const noColor=swatches.filter(sw=>!sw.style.backgroundColor&&!sw.style.background);return noColor.length===0?'PASS':'FAIL: '+noColor.length+' swatch(es) have no background color set';"}),
    },
    {
        "id": "cp-3",
        "name": "Clicking generate twice produces different swatches",
        "hidden": True,
        "weight": 2,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const btn=document.getElementById('generate-btn');const palette=document.getElementById('palette');if(!btn||!palette)return 'FAIL: missing elements';btn.click();const first=Array.from(palette.querySelectorAll('.color-swatch')).map(s=>s.style?.backgroundColor||s.textContent).join(',');btn.click();const second=Array.from(palette.querySelectorAll('.color-swatch')).map(s=>s.style?.backgroundColor||s.textContent).join(',');return first!==second?'PASS':'FAIL: two generates produced identical colors';"}),
    },
]

# ── QUIZ APP ────────────────────────────────────────────────────────────────
FRONTEND_TESTS["quiz-app"] = [
    {
        "id": "qa-1",
        "name": "All quiz UI elements exist on load",
        "hidden": False,
        "weight": 1,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const ids=['question','opt-0','opt-1','opt-2','opt-3','score-screen','final-score'];const missing=ids.filter(id=>!document.getElementById(id));return missing.length===0?'PASS':'FAIL: missing: '+missing.join(', ');"}),
    },
    {
        "id": "qa-2",
        "name": "Question text is non-empty on load",
        "hidden": False,
        "weight": 2,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const question=document.getElementById('question');if(!question)return 'FAIL: missing #question';const text=question.textContent.trim();return text.length>5?'PASS':'FAIL: #question is empty or too short on load. Got: \"'+text+'\"';"}),
    },
    {
        "id": "qa-3",
        "name": "Option buttons have text content",
        "hidden": False,
        "weight": 2,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const opts=[0,1,2,3].map(i=>document.getElementById('opt-'+i));if(opts.some(o=>!o))return 'FAIL: missing opt buttons';const empty=opts.filter(o=>!o.textContent.trim());return empty.length===0?'PASS':'FAIL: '+empty.length+' option button(s) have empty text';"}),
    },
    {
        "id": "qa-4",
        "name": "Clicking an option advances to next question or shows score",
        "hidden": True,
        "weight": 3,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const opt0=document.getElementById('opt-0');const question=document.getElementById('question');if(!opt0||!question)return 'FAIL: missing elements';const before=question.textContent.trim();opt0.click();return new Promise(resolve=>{setTimeout(()=>{const after=question.textContent.trim();const scoreScreen=document.getElementById('score-screen');const scoreVisible=scoreScreen&&scoreScreen.style.display!=='none'&&scoreScreen.offsetHeight>0;resolve((after!==before||scoreVisible)?'PASS':'FAIL: clicking option should advance question or show score screen');},100);});"}),
    },
]

# ── KANBAN BOARD ────────────────────────────────────────────────────────────
FRONTEND_TESTS["kanban-board"] = [
    {
        "id": "kb-1",
        "name": "Three kanban columns exist",
        "hidden": False,
        "weight": 1,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const cols=['col-todo','col-progress','col-done'];const missing=cols.filter(id=>!document.getElementById(id));return missing.length===0?'PASS':'FAIL: missing columns: '+missing.join(', ');"}),
    },
    {
        "id": "kb-2",
        "name": "Add button in Todo column creates a .kanban-card",
        "hidden": False,
        "weight": 2,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const todoCol=document.getElementById('col-todo');if(!todoCol)return 'FAIL: missing #col-todo';const inp=todoCol.querySelector('input');const btn=todoCol.querySelector('button');if(!inp||!btn)return 'FAIL: #col-todo missing input or button';const before=todoCol.querySelectorAll('.kanban-card').length;inp.value='Test Task';btn.click();const after=todoCol.querySelectorAll('.kanban-card').length;return after===before+1?'PASS':'FAIL: expected '+(before+1)+' cards, got '+after;"}),
    },
    {
        "id": "kb-3",
        "name": "Empty input does not add a card",
        "hidden": True,
        "weight": 1,
        "comparison_mode": "exact",
        "expected_output": "PASS\n",
        "stdin": json.dumps({"evaluation": "const todoCol=document.getElementById('col-todo');if(!todoCol)return 'FAIL: missing #col-todo';const inp=todoCol.querySelector('input');const btn=todoCol.querySelector('button');if(!inp||!btn)return 'FAIL: missing input or button';inp.value='';const before=todoCol.querySelectorAll('.kanban-card').length;btn.click();const after=todoCol.querySelectorAll('.kanban-card').length;return after===before?'PASS':'FAIL: empty input should not add cards';"}),
    },
]


def run():
    updated = 0
    failed = 0
    for slug, test_cases in FRONTEND_TESTS.items():
        result = col.update_one(
            {"slug": slug},
            {"$set": {"test_cases": test_cases}},
        )
        if result.matched_count:
            updated += 1
            print(f"  OK  {slug} => {len(test_cases)} behavioral tests")
        else:
            failed += 1
            print(f"  !!  NOT FOUND: {slug}")

    print(f"\nDone: {updated} updated, {failed} not found")


if __name__ == "__main__":
    run()
