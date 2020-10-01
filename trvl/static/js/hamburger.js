const mobileNav = document.querySelector('.mobile-nav');
const hamburger = document.getElementById('hamburger');
const close = document.getElementById('close');
const navBtns = document.querySelectorAll('.mobile-link');


hamburger.addEventListener('click', ()=> {
  mobileNav.style.display = 'block';
});

close.addEventListener('click', () => {
  mobileNav.style.display = 'none';
})


navBtns.forEach( (btn)=> {
  btn.addEventListener('click', ()=>{
    mobileNav.style.display = 'none';
  })
});