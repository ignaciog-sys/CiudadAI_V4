document.addEventListener('DOMContentLoaded', function () {
  // Transform native select.phone-prefix into custom dropdowns
  document.querySelectorAll('select.phone-prefix').forEach(function (select) {
    // hide native select
    select.style.display = 'none';

    // wrapper
    const wrapper = document.createElement('div');
    wrapper.className = 'phone-select-wrapper';

    // trigger button
    const trigger = document.createElement('button');
    trigger.type = 'button';
    trigger.className = 'custom-select-trigger';

    // initial value
    const selectedOption = select.options[select.selectedIndex] || select.options[0];
    trigger.textContent = selectedOption ? selectedOption.text : '';

    // options container
    const options = document.createElement('div');
    options.className = 'custom-options';

    // find related fields (hidden combined phone and local part)
    const form = select.closest('form');
    const hiddenTelefono = form ? form.querySelector('input[name="telefono"]') : null;
    const phoneLocalInput = form ? form.querySelector('input[name="phone_local"]') : null;

    function updateHiddenTelefono() {
      if (!hiddenTelefono) return;
      const local = phoneLocalInput && phoneLocalInput.value ? phoneLocalInput.value.trim() : '';
      hiddenTelefono.value = local ? `${select.value} ${local}` : select.value;
    }

    // listen to local input changes to keep hidden field updated
    if (phoneLocalInput) {
      phoneLocalInput.addEventListener('input', updateHiddenTelefono);
    }

    // build options
    Array.from(select.options).forEach(function (opt, idx) {
      const o = document.createElement('div');
      o.className = 'custom-option';
      o.dataset.value = opt.value;
      o.textContent = opt.text;
      if (opt.disabled) o.classList.add('disabled');
      if (opt.selected) o.classList.add('active');
      o.addEventListener('click', function (e) {
        // set selection
        select.value = o.dataset.value;
        // update trigger
        trigger.textContent = o.textContent;
        // update hidden telefono
        updateHiddenTelefono();
        // mark active
        options.querySelectorAll('.custom-option').forEach(function (c) { c.classList.remove('active'); });
        o.classList.add('active');
        // close
        wrapper.classList.remove('custom-select-open');
        select.dispatchEvent(new Event('change', { bubbles: true }));
      });
      options.appendChild(o);
    });

    // assemble
    wrapper.appendChild(trigger);
    wrapper.appendChild(options);

    // insert wrapper after select
    select.parentNode.insertBefore(wrapper, select.nextSibling);

    // open/close handling
    trigger.addEventListener('click', function (e) {
      e.stopPropagation();
      // close other custom selects
      document.querySelectorAll('.phone-select-wrapper').forEach(function (w) {
        if (w !== wrapper) w.classList.remove('custom-select-open');
      });
      wrapper.classList.toggle('custom-select-open');
    });

    // click outside closes
    document.addEventListener('click', function () { wrapper.classList.remove('custom-select-open'); });

    // keyboard navigation (basic)
    trigger.addEventListener('keydown', function (e) {
      const open = wrapper.classList.contains('custom-select-open');
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (!open) wrapper.classList.add('custom-select-open');
        else {
          const next = options.querySelector('.custom-option:not(.active)');
          if (next) { next.click(); }
        }
      }
    });
    // initialize hidden telefono with current values
    updateHiddenTelefono();
  });
});
