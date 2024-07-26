
let menu = document.getElementById("menu");
menu.addEventListener('click',function(e){
   document.querySelector('body').classList.toggle('mobile-nav-active');
   this.classList.toggle('fa-xmark');
})

let section=document.querySelector('.about');
let gspan=document.querySelectorAll('.progress span');


window.onscroll=function(){
 if(window.scrollY >= section.offsetTop + 350){
   gspan.forEach((span)=>{
     span.style.width = span.dataset.width;
   })
 }
}


//   active on scroll
let navLinks = document.querySelectorAll('nav ul li a');
let sections =document.querySelectorAll('section');

window.addEventListener('scroll',function(){
const scrollPos = window.scrollY + 20
sections.forEach(section=>{
if(scrollPos > section.offsetTop && scrollPos > (section.offsetTop )){
 navLinks.forEach(link=>{
   link.classList.remove('active');
   if(section.getAttribute('id')===link.getAttribute('href').substring(1)){
     link.classList.add('active')
   }
 });
}
});
});

// عند النقر على الزر
function showModal() {
 var modal = document.getElementById("uplodeImageModal");
 modal.style.display = "block";
}

// عند النقر على زر الإغلاق
function closeModal() {
 var modal = document.getElementById("uplodeImageModal");
 modal.style.display = "none";
}

window.onclick = function(event) {
 var modal = document.getElementById("uplodeImageModal");
 if (event.target === modal) {
   modal.style.display = "none";
 }
}


document.getElementById("saveButton").addEventListener("click", function () {
 document.querySelector("form").submit();
 var bottonstart = document.getElementById('bottonstart');
 bottonstart.innerHTML = `<button class="btn btn-success w-100" type="button" disabled>
     <span class="spinner-border spinner-border-sm "  role="status" aria-hidden="true"></span>
     Loading...
   </button>`;
});

function highlightDropArea() {
  dropArea.classList.add('highlight');
}

function unhighlightDropArea() {
  dropArea.classList.remove('highlight');
}
function handleFileDrop(event) {
  event.preventDefault();
  unhighlightDropArea();

  var files = event.dataTransfer.files;
  if (files.length > 0) {
    fileInput.files = event.dataTransfer.files;
    dropArea.classList.add('received');
  }
}

function handleFileInputChange(event) {
  var files = event.target.files;
  if (files.length > 0) {
    console.log('Selected file:', files[0].name);
    dropArea.classList.add('received');
  }
}

function handleSaveButtonClick() {
  var files = fileInput.files;
  if (files.length > 0) {
    // Save the file here
    console.log('Saving file:', files[0].name);
  }
}

dropArea.addEventListener('dragenter', highlightDropArea);
dropArea.addEventListener('dragleave', unhighlightDropArea);
dropArea.addEventListener('dragover', function(event) {
  event.preventDefault();
});
dropArea.addEventListener('drop', handleFileDrop);
fileInput.addEventListener('change', handleFileInputChange);
saveButton.addEventListener('click', handleSaveButtonClick);

// end add Image Form
