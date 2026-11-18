// Léim — small site script
// Waitlist form: sends sign-ups to the Léim MailerLite form
// (account 2794931, form "Léim – JC Spanish free guide (website)"; since 15 Nov 2026 the freebie is the parent college guide).
var ML_URL = 'https://assets.mailerlite.com/jsonp/2794931/forms/204102674478531601/subscribe';
document.querySelectorAll('form.waitlist').forEach(function (form) {
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var msg = form.parentElement.querySelector('.form-msg');
    var err = form.querySelector('.form-err');
    if (!err) {
      err = document.createElement('p');
      err.className = 'form-err small';
      err.setAttribute('role', 'alert');
      form.appendChild(err);
    }
    err.textContent = '';
    if (!form.checkValidity()) {
      err.textContent = 'Please add your first name and email.';
      return;
    }
    var btn = form.querySelector('button[type=submit]');
    btn.disabled = true;
    var data = new FormData(form);
    data.append('ml-submit', '1');
    data.append('anticsrf', 'true');
    var done = function () {
      form.style.display = 'none';
      if (msg) { msg.style.display = 'block'; msg.focus(); }
    };
    fetch(ML_URL, { method: 'POST', body: data })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        if (j && j.success) { done(); }
        else { throw new Error('rejected'); }
      })
      .catch(function () {
        btn.disabled = false;
        err.textContent = 'Sorry, that didn\'t go through. Please try again, or email hello@leim.ie.';
      });
  });
});

// Year tabs on the Spanish page
var tabs = document.querySelectorAll('.years button');
tabs.forEach(function (btn) {
  btn.addEventListener('click', function () {
    tabs.forEach(function (b) {
      b.setAttribute('aria-selected', b === btn ? 'true' : 'false');
      var panel = document.getElementById(b.getAttribute('aria-controls'));
      if (panel) panel.hidden = b !== btn;
    });
  });
});

// Footer year
document.querySelectorAll('.yr').forEach(function (el) { el.textContent = new Date().getFullYear(); });

// Visitor stats (GoatCounter: leim.goatcounter.com). No cookies, no personal data.
(function () {
  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://gc.zgo.at/count.js';
  s.setAttribute('data-goatcounter', 'https://leim.goatcounter.com/count');
  document.head.appendChild(s);
})();

// Phones: tables with 3+ columns become stacked cards (see styles.css), each value labelled with its column name
document.querySelectorAll('.table-wrap > table').forEach(function (t) {
  var heads = t.querySelectorAll('thead th');
  if (heads.length < 3) return;
  t.classList.add('stack');
  t.querySelectorAll('tbody tr').forEach(function (tr) {
    var col = 0;
    Array.prototype.forEach.call(tr.children, function (td) {
      var span = td.colSpan || 1;
      var label = span > 1 ? '' : (heads[col] ? heads[col].textContent.trim() : '');
      if (label) td.setAttribute('data-label', label);
      col += span;
    });
  });
});
