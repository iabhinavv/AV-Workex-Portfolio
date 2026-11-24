/* Shared keyboard-accessible mobile navigation. */
(() => {
  'use strict';
  const menu = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#main-nav');
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('open', open);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && nav.classList.contains('open')) {
      nav.classList.remove('open');
      menu.setAttribute('aria-expanded', 'false');
      menu.focus();
    }
  });
  const contents=document.querySelector('.document-contents');
  if(contents&&matchMedia('(max-width:960px)').matches) contents.open=false;
})();
