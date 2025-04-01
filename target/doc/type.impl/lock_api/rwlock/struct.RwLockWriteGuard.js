(function() {
    var type_impls = Object.fromEntries([["parking_lot",[["<details class=\"toggle implementors-toggle\" open><summary><section id=\"impl-Debug-for-RwLockWriteGuard%3C'a,+R,+T%3E\" class=\"impl\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1719\">Source</a><a href=\"#impl-Debug-for-RwLockWriteGuard%3C'a,+R,+T%3E\" class=\"anchor\">§</a><h3 class=\"code-header\">impl&lt;'a, R, T&gt; <a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/fmt/trait.Debug.html\" title=\"trait core::fmt::Debug\">Debug</a> for <a class=\"struct\" href=\"lock_api/rwlock/struct.RwLockWriteGuard.html\" title=\"struct lock_api::rwlock::RwLockWriteGuard\">RwLockWriteGuard</a>&lt;'a, R, T&gt;<div class=\"where\">where\n    R: <a class=\"trait\" href=\"lock_api/rwlock/trait.RawRwLock.html\" title=\"trait lock_api::rwlock::RawRwLock\">RawRwLock</a> + 'a,\n    T: <a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/fmt/trait.Debug.html\" title=\"trait core::fmt::Debug\">Debug</a> + 'a + ?<a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/marker/trait.Sized.html\" title=\"trait core::marker::Sized\">Sized</a>,</div></h3></section></summary><div class=\"impl-items\"><details class=\"toggle method-toggle\" open><summary><section id=\"method.fmt\" class=\"method trait-impl\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1720\">Source</a><a href=\"#method.fmt\" class=\"anchor\">§</a><h4 class=\"code-header\">fn <a href=\"https://doc.rust-lang.org/1.85.1/core/fmt/trait.Debug.html#tymethod.fmt\" class=\"fn\">fmt</a>(&amp;self, f: &amp;mut <a class=\"struct\" href=\"https://doc.rust-lang.org/1.85.1/core/fmt/struct.Formatter.html\" title=\"struct core::fmt::Formatter\">Formatter</a>&lt;'_&gt;) -&gt; <a class=\"enum\" href=\"https://doc.rust-lang.org/1.85.1/core/result/enum.Result.html\" title=\"enum core::result::Result\">Result</a>&lt;<a class=\"primitive\" href=\"https://doc.rust-lang.org/1.85.1/std/primitive.unit.html\">()</a>, <a class=\"struct\" href=\"https://doc.rust-lang.org/1.85.1/core/fmt/struct.Error.html\" title=\"struct core::fmt::Error\">Error</a>&gt;</h4></section></summary><div class='docblock'>Formats the value using the given formatter. <a href=\"https://doc.rust-lang.org/1.85.1/core/fmt/trait.Debug.html#tymethod.fmt\">Read more</a></div></details></div></details>","Debug","parking_lot::rwlock::RwLockWriteGuard"],["<details class=\"toggle implementors-toggle\" open><summary><section id=\"impl-Deref-for-RwLockWriteGuard%3C'a,+R,+T%3E\" class=\"impl\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1694\">Source</a><a href=\"#impl-Deref-for-RwLockWriteGuard%3C'a,+R,+T%3E\" class=\"anchor\">§</a><h3 class=\"code-header\">impl&lt;'a, R, T&gt; <a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/ops/deref/trait.Deref.html\" title=\"trait core::ops::deref::Deref\">Deref</a> for <a class=\"struct\" href=\"lock_api/rwlock/struct.RwLockWriteGuard.html\" title=\"struct lock_api::rwlock::RwLockWriteGuard\">RwLockWriteGuard</a>&lt;'a, R, T&gt;<div class=\"where\">where\n    R: <a class=\"trait\" href=\"lock_api/rwlock/trait.RawRwLock.html\" title=\"trait lock_api::rwlock::RawRwLock\">RawRwLock</a> + 'a,\n    T: 'a + ?<a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/marker/trait.Sized.html\" title=\"trait core::marker::Sized\">Sized</a>,</div></h3></section></summary><div class=\"impl-items\"><details class=\"toggle\" open><summary><section id=\"associatedtype.Target\" class=\"associatedtype trait-impl\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1695\">Source</a><a href=\"#associatedtype.Target\" class=\"anchor\">§</a><h4 class=\"code-header\">type <a href=\"https://doc.rust-lang.org/1.85.1/core/ops/deref/trait.Deref.html#associatedtype.Target\" class=\"associatedtype\">Target</a> = T</h4></section></summary><div class='docblock'>The resulting type after dereferencing.</div></details><details class=\"toggle method-toggle\" open><summary><section id=\"method.deref\" class=\"method trait-impl\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1697\">Source</a><a href=\"#method.deref\" class=\"anchor\">§</a><h4 class=\"code-header\">fn <a href=\"https://doc.rust-lang.org/1.85.1/core/ops/deref/trait.Deref.html#tymethod.deref\" class=\"fn\">deref</a>(&amp;self) -&gt; <a class=\"primitive\" href=\"https://doc.rust-lang.org/1.85.1/std/primitive.reference.html\">&amp;T</a></h4></section></summary><div class='docblock'>Dereferences the value.</div></details></div></details>","Deref","parking_lot::rwlock::RwLockWriteGuard"],["<details class=\"toggle implementors-toggle\" open><summary><section id=\"impl-DerefMut-for-RwLockWriteGuard%3C'a,+R,+T%3E\" class=\"impl\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1702\">Source</a><a href=\"#impl-DerefMut-for-RwLockWriteGuard%3C'a,+R,+T%3E\" class=\"anchor\">§</a><h3 class=\"code-header\">impl&lt;'a, R, T&gt; <a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/ops/deref/trait.DerefMut.html\" title=\"trait core::ops::deref::DerefMut\">DerefMut</a> for <a class=\"struct\" href=\"lock_api/rwlock/struct.RwLockWriteGuard.html\" title=\"struct lock_api::rwlock::RwLockWriteGuard\">RwLockWriteGuard</a>&lt;'a, R, T&gt;<div class=\"where\">where\n    R: <a class=\"trait\" href=\"lock_api/rwlock/trait.RawRwLock.html\" title=\"trait lock_api::rwlock::RawRwLock\">RawRwLock</a> + 'a,\n    T: 'a + ?<a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/marker/trait.Sized.html\" title=\"trait core::marker::Sized\">Sized</a>,</div></h3></section></summary><div class=\"impl-items\"><details class=\"toggle method-toggle\" open><summary><section id=\"method.deref_mut\" class=\"method trait-impl\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1704\">Source</a><a href=\"#method.deref_mut\" class=\"anchor\">§</a><h4 class=\"code-header\">fn <a href=\"https://doc.rust-lang.org/1.85.1/core/ops/deref/trait.DerefMut.html#tymethod.deref_mut\" class=\"fn\">deref_mut</a>(&amp;mut self) -&gt; <a class=\"primitive\" href=\"https://doc.rust-lang.org/1.85.1/std/primitive.reference.html\">&amp;mut T</a></h4></section></summary><div class='docblock'>Mutably dereferences the value.</div></details></div></details>","DerefMut","parking_lot::rwlock::RwLockWriteGuard"],["<details class=\"toggle implementors-toggle\" open><summary><section id=\"impl-Display-for-RwLockWriteGuard%3C'a,+R,+T%3E\" class=\"impl\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1725-1726\">Source</a><a href=\"#impl-Display-for-RwLockWriteGuard%3C'a,+R,+T%3E\" class=\"anchor\">§</a><h3 class=\"code-header\">impl&lt;'a, R, T&gt; <a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/fmt/trait.Display.html\" title=\"trait core::fmt::Display\">Display</a> for <a class=\"struct\" href=\"lock_api/rwlock/struct.RwLockWriteGuard.html\" title=\"struct lock_api::rwlock::RwLockWriteGuard\">RwLockWriteGuard</a>&lt;'a, R, T&gt;<div class=\"where\">where\n    R: <a class=\"trait\" href=\"lock_api/rwlock/trait.RawRwLock.html\" title=\"trait lock_api::rwlock::RawRwLock\">RawRwLock</a> + 'a,\n    T: <a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/fmt/trait.Display.html\" title=\"trait core::fmt::Display\">Display</a> + 'a + ?<a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/marker/trait.Sized.html\" title=\"trait core::marker::Sized\">Sized</a>,</div></h3></section></summary><div class=\"impl-items\"><details class=\"toggle method-toggle\" open><summary><section id=\"method.fmt\" class=\"method trait-impl\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1728\">Source</a><a href=\"#method.fmt\" class=\"anchor\">§</a><h4 class=\"code-header\">fn <a href=\"https://doc.rust-lang.org/1.85.1/core/fmt/trait.Display.html#tymethod.fmt\" class=\"fn\">fmt</a>(&amp;self, f: &amp;mut <a class=\"struct\" href=\"https://doc.rust-lang.org/1.85.1/core/fmt/struct.Formatter.html\" title=\"struct core::fmt::Formatter\">Formatter</a>&lt;'_&gt;) -&gt; <a class=\"enum\" href=\"https://doc.rust-lang.org/1.85.1/core/result/enum.Result.html\" title=\"enum core::result::Result\">Result</a>&lt;<a class=\"primitive\" href=\"https://doc.rust-lang.org/1.85.1/std/primitive.unit.html\">()</a>, <a class=\"struct\" href=\"https://doc.rust-lang.org/1.85.1/core/fmt/struct.Error.html\" title=\"struct core::fmt::Error\">Error</a>&gt;</h4></section></summary><div class='docblock'>Formats the value using the given formatter. <a href=\"https://doc.rust-lang.org/1.85.1/core/fmt/trait.Display.html#tymethod.fmt\">Read more</a></div></details></div></details>","Display","parking_lot::rwlock::RwLockWriteGuard"],["<details class=\"toggle implementors-toggle\" open><summary><section id=\"impl-Drop-for-RwLockWriteGuard%3C'a,+R,+T%3E\" class=\"impl\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1709\">Source</a><a href=\"#impl-Drop-for-RwLockWriteGuard%3C'a,+R,+T%3E\" class=\"anchor\">§</a><h3 class=\"code-header\">impl&lt;'a, R, T&gt; <a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/ops/drop/trait.Drop.html\" title=\"trait core::ops::drop::Drop\">Drop</a> for <a class=\"struct\" href=\"lock_api/rwlock/struct.RwLockWriteGuard.html\" title=\"struct lock_api::rwlock::RwLockWriteGuard\">RwLockWriteGuard</a>&lt;'a, R, T&gt;<div class=\"where\">where\n    R: <a class=\"trait\" href=\"lock_api/rwlock/trait.RawRwLock.html\" title=\"trait lock_api::rwlock::RawRwLock\">RawRwLock</a> + 'a,\n    T: 'a + ?<a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/marker/trait.Sized.html\" title=\"trait core::marker::Sized\">Sized</a>,</div></h3></section></summary><div class=\"impl-items\"><details class=\"toggle method-toggle\" open><summary><section id=\"method.drop\" class=\"method trait-impl\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1711\">Source</a><a href=\"#method.drop\" class=\"anchor\">§</a><h4 class=\"code-header\">fn <a href=\"https://doc.rust-lang.org/1.85.1/core/ops/drop/trait.Drop.html#tymethod.drop\" class=\"fn\">drop</a>(&amp;mut self)</h4></section></summary><div class='docblock'>Executes the destructor for this type. <a href=\"https://doc.rust-lang.org/1.85.1/core/ops/drop/trait.Drop.html#tymethod.drop\">Read more</a></div></details></div></details>","Drop","parking_lot::rwlock::RwLockWriteGuard"],["<details class=\"toggle implementors-toggle\" open><summary><section id=\"impl-RwLockWriteGuard%3C'a,+R,+T%3E\" class=\"impl\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1523\">Source</a><a href=\"#impl-RwLockWriteGuard%3C'a,+R,+T%3E\" class=\"anchor\">§</a><h3 class=\"code-header\">impl&lt;'a, R, T&gt; <a class=\"struct\" href=\"lock_api/rwlock/struct.RwLockWriteGuard.html\" title=\"struct lock_api::rwlock::RwLockWriteGuard\">RwLockWriteGuard</a>&lt;'a, R, T&gt;<div class=\"where\">where\n    R: <a class=\"trait\" href=\"lock_api/rwlock/trait.RawRwLock.html\" title=\"trait lock_api::rwlock::RawRwLock\">RawRwLock</a> + 'a,\n    T: 'a + ?<a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/marker/trait.Sized.html\" title=\"trait core::marker::Sized\">Sized</a>,</div></h3></section></summary><div class=\"impl-items\"><details class=\"toggle method-toggle\" open><summary><section id=\"method.rwlock\" class=\"method\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1525\">Source</a><h4 class=\"code-header\">pub fn <a href=\"lock_api/rwlock/struct.RwLockWriteGuard.html#tymethod.rwlock\" class=\"fn\">rwlock</a>(s: &amp;<a class=\"struct\" href=\"lock_api/rwlock/struct.RwLockWriteGuard.html\" title=\"struct lock_api::rwlock::RwLockWriteGuard\">RwLockWriteGuard</a>&lt;'a, R, T&gt;) -&gt; &amp;'a <a class=\"struct\" href=\"lock_api/rwlock/struct.RwLock.html\" title=\"struct lock_api::rwlock::RwLock\">RwLock</a>&lt;R, T&gt;</h4></section></summary><div class=\"docblock\"><p>Returns a reference to the original reader-writer lock object.</p>\n</div></details><details class=\"toggle method-toggle\" open><summary><section id=\"method.map\" class=\"method\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1538-1540\">Source</a><h4 class=\"code-header\">pub fn <a href=\"lock_api/rwlock/struct.RwLockWriteGuard.html#tymethod.map\" class=\"fn\">map</a>&lt;U, F&gt;(\n    s: <a class=\"struct\" href=\"lock_api/rwlock/struct.RwLockWriteGuard.html\" title=\"struct lock_api::rwlock::RwLockWriteGuard\">RwLockWriteGuard</a>&lt;'a, R, T&gt;,\n    f: F,\n) -&gt; <a class=\"struct\" href=\"lock_api/rwlock/struct.MappedRwLockWriteGuard.html\" title=\"struct lock_api::rwlock::MappedRwLockWriteGuard\">MappedRwLockWriteGuard</a>&lt;'a, R, U&gt;<div class=\"where\">where\n    F: <a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/ops/function/trait.FnOnce.html\" title=\"trait core::ops::function::FnOnce\">FnOnce</a>(<a class=\"primitive\" href=\"https://doc.rust-lang.org/1.85.1/std/primitive.reference.html\">&amp;mut T</a>) -&gt; <a class=\"primitive\" href=\"https://doc.rust-lang.org/1.85.1/std/primitive.reference.html\">&amp;mut U</a>,\n    U: ?<a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/marker/trait.Sized.html\" title=\"trait core::marker::Sized\">Sized</a>,</div></h4></section></summary><div class=\"docblock\"><p>Make a new <code>MappedRwLockWriteGuard</code> for a component of the locked data.</p>\n<p>This operation cannot fail as the <code>RwLockWriteGuard</code> passed\nin already locked the data.</p>\n<p>This is an associated function that needs to be\nused as <code>RwLockWriteGuard::map(...)</code>. A method would interfere with methods of\nthe same name on the contents of the locked data.</p>\n</div></details><details class=\"toggle method-toggle\" open><summary><section id=\"method.try_map\" class=\"method\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1562-1564\">Source</a><h4 class=\"code-header\">pub fn <a href=\"lock_api/rwlock/struct.RwLockWriteGuard.html#tymethod.try_map\" class=\"fn\">try_map</a>&lt;U, F&gt;(\n    s: <a class=\"struct\" href=\"lock_api/rwlock/struct.RwLockWriteGuard.html\" title=\"struct lock_api::rwlock::RwLockWriteGuard\">RwLockWriteGuard</a>&lt;'a, R, T&gt;,\n    f: F,\n) -&gt; <a class=\"enum\" href=\"https://doc.rust-lang.org/1.85.1/core/result/enum.Result.html\" title=\"enum core::result::Result\">Result</a>&lt;<a class=\"struct\" href=\"lock_api/rwlock/struct.MappedRwLockWriteGuard.html\" title=\"struct lock_api::rwlock::MappedRwLockWriteGuard\">MappedRwLockWriteGuard</a>&lt;'a, R, U&gt;, <a class=\"struct\" href=\"lock_api/rwlock/struct.RwLockWriteGuard.html\" title=\"struct lock_api::rwlock::RwLockWriteGuard\">RwLockWriteGuard</a>&lt;'a, R, T&gt;&gt;<div class=\"where\">where\n    F: <a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/ops/function/trait.FnOnce.html\" title=\"trait core::ops::function::FnOnce\">FnOnce</a>(<a class=\"primitive\" href=\"https://doc.rust-lang.org/1.85.1/std/primitive.reference.html\">&amp;mut T</a>) -&gt; <a class=\"enum\" href=\"https://doc.rust-lang.org/1.85.1/core/option/enum.Option.html\" title=\"enum core::option::Option\">Option</a>&lt;<a class=\"primitive\" href=\"https://doc.rust-lang.org/1.85.1/std/primitive.reference.html\">&amp;mut U</a>&gt;,\n    U: ?<a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/marker/trait.Sized.html\" title=\"trait core::marker::Sized\">Sized</a>,</div></h4></section></summary><div class=\"docblock\"><p>Attempts to make  a new <code>MappedRwLockWriteGuard</code> for a component of the\nlocked data. The original guard is return if the closure returns <code>None</code>.</p>\n<p>This operation cannot fail as the <code>RwLockWriteGuard</code> passed\nin already locked the data.</p>\n<p>This is an associated function that needs to be\nused as <code>RwLockWriteGuard::try_map(...)</code>. A method would interfere with methods of\nthe same name on the contents of the locked data.</p>\n</div></details><details class=\"toggle method-toggle\" open><summary><section id=\"method.unlocked\" class=\"method\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1584-1586\">Source</a><h4 class=\"code-header\">pub fn <a href=\"lock_api/rwlock/struct.RwLockWriteGuard.html#tymethod.unlocked\" class=\"fn\">unlocked</a>&lt;F, U&gt;(s: &amp;mut <a class=\"struct\" href=\"lock_api/rwlock/struct.RwLockWriteGuard.html\" title=\"struct lock_api::rwlock::RwLockWriteGuard\">RwLockWriteGuard</a>&lt;'a, R, T&gt;, f: F) -&gt; U<div class=\"where\">where\n    F: <a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/ops/function/trait.FnOnce.html\" title=\"trait core::ops::function::FnOnce\">FnOnce</a>() -&gt; U,</div></h4></section></summary><div class=\"docblock\"><p>Temporarily unlocks the <code>RwLock</code> to execute the given function.</p>\n<p>This is safe because <code>&amp;mut</code> guarantees that there exist no other\nreferences to the data protected by the <code>RwLock</code>.</p>\n</div></details></div></details>",0,"parking_lot::rwlock::RwLockWriteGuard"],["<details class=\"toggle implementors-toggle\" open><summary><section id=\"impl-RwLockWriteGuard%3C'a,+R,+T%3E\" class=\"impl\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1597\">Source</a><a href=\"#impl-RwLockWriteGuard%3C'a,+R,+T%3E\" class=\"anchor\">§</a><h3 class=\"code-header\">impl&lt;'a, R, T&gt; <a class=\"struct\" href=\"lock_api/rwlock/struct.RwLockWriteGuard.html\" title=\"struct lock_api::rwlock::RwLockWriteGuard\">RwLockWriteGuard</a>&lt;'a, R, T&gt;<div class=\"where\">where\n    R: <a class=\"trait\" href=\"lock_api/rwlock/trait.RawRwLockDowngrade.html\" title=\"trait lock_api::rwlock::RawRwLockDowngrade\">RawRwLockDowngrade</a> + 'a,\n    T: 'a + ?<a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/marker/trait.Sized.html\" title=\"trait core::marker::Sized\">Sized</a>,</div></h3></section></summary><div class=\"impl-items\"><details class=\"toggle method-toggle\" open><summary><section id=\"method.downgrade\" class=\"method\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1604\">Source</a><h4 class=\"code-header\">pub fn <a href=\"lock_api/rwlock/struct.RwLockWriteGuard.html#tymethod.downgrade\" class=\"fn\">downgrade</a>(s: <a class=\"struct\" href=\"lock_api/rwlock/struct.RwLockWriteGuard.html\" title=\"struct lock_api::rwlock::RwLockWriteGuard\">RwLockWriteGuard</a>&lt;'a, R, T&gt;) -&gt; <a class=\"struct\" href=\"lock_api/rwlock/struct.RwLockReadGuard.html\" title=\"struct lock_api::rwlock::RwLockReadGuard\">RwLockReadGuard</a>&lt;'a, R, T&gt;</h4></section></summary><div class=\"docblock\"><p>Atomically downgrades a write lock into a read lock without allowing any\nwriters to take exclusive access of the lock in the meantime.</p>\n<p>Note that if there are any writers currently waiting to take the lock\nthen other readers may not be able to acquire the lock even if it was\ndowngraded.</p>\n</div></details></div></details>",0,"parking_lot::rwlock::RwLockWriteGuard"],["<details class=\"toggle implementors-toggle\" open><summary><section id=\"impl-RwLockWriteGuard%3C'a,+R,+T%3E\" class=\"impl\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1618\">Source</a><a href=\"#impl-RwLockWriteGuard%3C'a,+R,+T%3E\" class=\"anchor\">§</a><h3 class=\"code-header\">impl&lt;'a, R, T&gt; <a class=\"struct\" href=\"lock_api/rwlock/struct.RwLockWriteGuard.html\" title=\"struct lock_api::rwlock::RwLockWriteGuard\">RwLockWriteGuard</a>&lt;'a, R, T&gt;<div class=\"where\">where\n    R: <a class=\"trait\" href=\"lock_api/rwlock/trait.RawRwLockUpgradeDowngrade.html\" title=\"trait lock_api::rwlock::RawRwLockUpgradeDowngrade\">RawRwLockUpgradeDowngrade</a> + 'a,\n    T: 'a + ?<a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/marker/trait.Sized.html\" title=\"trait core::marker::Sized\">Sized</a>,</div></h3></section></summary><div class=\"impl-items\"><details class=\"toggle method-toggle\" open><summary><section id=\"method.downgrade_to_upgradable\" class=\"method\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1625\">Source</a><h4 class=\"code-header\">pub fn <a href=\"lock_api/rwlock/struct.RwLockWriteGuard.html#tymethod.downgrade_to_upgradable\" class=\"fn\">downgrade_to_upgradable</a>(\n    s: <a class=\"struct\" href=\"lock_api/rwlock/struct.RwLockWriteGuard.html\" title=\"struct lock_api::rwlock::RwLockWriteGuard\">RwLockWriteGuard</a>&lt;'a, R, T&gt;,\n) -&gt; <a class=\"struct\" href=\"lock_api/rwlock/struct.RwLockUpgradableReadGuard.html\" title=\"struct lock_api::rwlock::RwLockUpgradableReadGuard\">RwLockUpgradableReadGuard</a>&lt;'a, R, T&gt;</h4></section></summary><div class=\"docblock\"><p>Atomically downgrades a write lock into an upgradable read lock without allowing any\nwriters to take exclusive access of the lock in the meantime.</p>\n<p>Note that if there are any writers currently waiting to take the lock\nthen other readers may not be able to acquire the lock even if it was\ndowngraded.</p>\n</div></details></div></details>",0,"parking_lot::rwlock::RwLockWriteGuard"],["<details class=\"toggle implementors-toggle\" open><summary><section id=\"impl-RwLockWriteGuard%3C'a,+R,+T%3E\" class=\"impl\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1639\">Source</a><a href=\"#impl-RwLockWriteGuard%3C'a,+R,+T%3E\" class=\"anchor\">§</a><h3 class=\"code-header\">impl&lt;'a, R, T&gt; <a class=\"struct\" href=\"lock_api/rwlock/struct.RwLockWriteGuard.html\" title=\"struct lock_api::rwlock::RwLockWriteGuard\">RwLockWriteGuard</a>&lt;'a, R, T&gt;<div class=\"where\">where\n    R: <a class=\"trait\" href=\"lock_api/rwlock/trait.RawRwLockFair.html\" title=\"trait lock_api::rwlock::RawRwLockFair\">RawRwLockFair</a> + 'a,\n    T: 'a + ?<a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/marker/trait.Sized.html\" title=\"trait core::marker::Sized\">Sized</a>,</div></h3></section></summary><div class=\"impl-items\"><details class=\"toggle method-toggle\" open><summary><section id=\"method.unlock_fair\" class=\"method\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1653\">Source</a><h4 class=\"code-header\">pub fn <a href=\"lock_api/rwlock/struct.RwLockWriteGuard.html#tymethod.unlock_fair\" class=\"fn\">unlock_fair</a>(s: <a class=\"struct\" href=\"lock_api/rwlock/struct.RwLockWriteGuard.html\" title=\"struct lock_api::rwlock::RwLockWriteGuard\">RwLockWriteGuard</a>&lt;'a, R, T&gt;)</h4></section></summary><div class=\"docblock\"><p>Unlocks the <code>RwLock</code> using a fair unlock protocol.</p>\n<p>By default, <code>RwLock</code> is unfair and allow the current thread to re-lock\nthe <code>RwLock</code> before another has the chance to acquire the lock, even if\nthat thread has been blocked on the <code>RwLock</code> for a long time. This is\nthe default because it allows much higher throughput as it avoids\nforcing a context switch on every <code>RwLock</code> unlock. This can result in one\nthread acquiring a <code>RwLock</code> many more times than other threads.</p>\n<p>However in some cases it can be beneficial to ensure fairness by forcing\nthe lock to pass on to a waiting thread if there is one. This is done by\nusing this method instead of dropping the <code>RwLockWriteGuard</code> normally.</p>\n</div></details><details class=\"toggle method-toggle\" open><summary><section id=\"method.unlocked_fair\" class=\"method\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1668-1670\">Source</a><h4 class=\"code-header\">pub fn <a href=\"lock_api/rwlock/struct.RwLockWriteGuard.html#tymethod.unlocked_fair\" class=\"fn\">unlocked_fair</a>&lt;F, U&gt;(s: &amp;mut <a class=\"struct\" href=\"lock_api/rwlock/struct.RwLockWriteGuard.html\" title=\"struct lock_api::rwlock::RwLockWriteGuard\">RwLockWriteGuard</a>&lt;'a, R, T&gt;, f: F) -&gt; U<div class=\"where\">where\n    F: <a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/ops/function/trait.FnOnce.html\" title=\"trait core::ops::function::FnOnce\">FnOnce</a>() -&gt; U,</div></h4></section></summary><div class=\"docblock\"><p>Temporarily unlocks the <code>RwLock</code> to execute the given function.</p>\n<p>The <code>RwLock</code> is unlocked a fair unlock protocol.</p>\n<p>This is safe because <code>&amp;mut</code> guarantees that there exist no other\nreferences to the data protected by the <code>RwLock</code>.</p>\n</div></details><details class=\"toggle method-toggle\" open><summary><section id=\"method.bump\" class=\"method\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1686\">Source</a><h4 class=\"code-header\">pub fn <a href=\"lock_api/rwlock/struct.RwLockWriteGuard.html#tymethod.bump\" class=\"fn\">bump</a>(s: &amp;mut <a class=\"struct\" href=\"lock_api/rwlock/struct.RwLockWriteGuard.html\" title=\"struct lock_api::rwlock::RwLockWriteGuard\">RwLockWriteGuard</a>&lt;'a, R, T&gt;)</h4></section></summary><div class=\"docblock\"><p>Temporarily yields the <code>RwLock</code> to a waiting thread if there is one.</p>\n<p>This method is functionally equivalent to calling <code>unlock_fair</code> followed\nby <code>write</code>, however it can be much more efficient in the case where there\nare no waiting threads.</p>\n</div></details></div></details>",0,"parking_lot::rwlock::RwLockWriteGuard"],["<section id=\"impl-Sync-for-RwLockWriteGuard%3C'_,+R,+T%3E\" class=\"impl\"><a class=\"src rightside\" href=\"src/lock_api/rwlock.rs.html#1521\">Source</a><a href=\"#impl-Sync-for-RwLockWriteGuard%3C'_,+R,+T%3E\" class=\"anchor\">§</a><h3 class=\"code-header\">impl&lt;R, T&gt; <a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/marker/trait.Sync.html\" title=\"trait core::marker::Sync\">Sync</a> for <a class=\"struct\" href=\"lock_api/rwlock/struct.RwLockWriteGuard.html\" title=\"struct lock_api::rwlock::RwLockWriteGuard\">RwLockWriteGuard</a>&lt;'_, R, T&gt;<div class=\"where\">where\n    R: <a class=\"trait\" href=\"lock_api/rwlock/trait.RawRwLock.html\" title=\"trait lock_api::rwlock::RawRwLock\">RawRwLock</a> + <a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/marker/trait.Sync.html\" title=\"trait core::marker::Sync\">Sync</a>,\n    T: <a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/marker/trait.Sync.html\" title=\"trait core::marker::Sync\">Sync</a> + ?<a class=\"trait\" href=\"https://doc.rust-lang.org/1.85.1/core/marker/trait.Sized.html\" title=\"trait core::marker::Sized\">Sized</a>,</div></h3></section>","Sync","parking_lot::rwlock::RwLockWriteGuard"]]]]);
    if (window.register_type_impls) {
        window.register_type_impls(type_impls);
    } else {
        window.pending_type_impls = type_impls;
    }
})()
//{"start":55,"fragment_lengths":[26547]}