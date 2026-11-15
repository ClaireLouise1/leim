# Notes for Claude (Léim)

## ⚠ Payhip: check the store before EVERY Payhip action
Claire-Louise has more than one Payhip store: **Léim** (payhip.com/Leim), **Spraoi Learning** (payhip.com/SpraoiLearning) and Lessons That Click. The Claude browser pane is shared by ALL chats, and Payhip keeps only one account signed in at a time, so another chat may have switched it.

1. **Before adding, editing or deleting any product**, check which store the pane is in: on payhip.com run `fetch('/products').then(r=>r.text())` and see which store link (`payhip.com/SpraoiLearning` or `payhip.com/Leim`) appears. If it isn't the store you need, **stop** and ask her to switch accounts (she types the password herself).
2. **After creating a product**, fetch its `payhip.com/b/<code>` page with `{credentials:'omit'}` and confirm it's sold by the right store.
3. **If you switch the pane to another store, tell her at the end** which account it's now signed in to, so the next chat doesn't sell in the wrong store.

(Rule added 15 Nov 2026 after 21 Léim products were created in the Spraoi Learning store by mistake.)

The full Léim job list lives in the claude.ai project "LEIM REVISION" (claude/leim-todo.md).
