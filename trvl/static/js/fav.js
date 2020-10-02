let favForm = document.querySelector('.fav-form-outer');
let closeBtns = document.querySelectorAll('.close-fav-form');
console.log('CLOSE BTNS',closeBtns)
closeBtns.forEach((btn)=>{
  btn.addEventListener('click', ()=>{
    favForm.style.display = 'none';
  })
})

let favBtns = document.querySelectorAll('.fav-btn');
console.log('FAV BTNS', favBtns);

favBtns.forEach((btn)=> {
  btn.addEventListener('click', ()=> {
    console.log(btn.getAttribute(`fav-btn-${i}`))
  });
});