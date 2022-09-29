


function buscador() {
  var input, filter, ul, li, a, i, txtValue;
  input = document.getElementById('search');
  filter = input.value.toUpperCase();
  ul = document.getElementById("lista");
  li = ul.getElementsByTagName('li');

  for (i = 0; i < li.length; i++) {
    a = li[i].getElementsByTagName("button")[0];
    txtValue = a.textContent || a.innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
}
function buscador2() {
  var input, filter, ul, li, a, i, txtValue;
  input = document.getElementById('search');
  filter = input.value.toUpperCase();
  ul = document.getElementById("lista");
  li = ul.getElementsByTagName('li');

  for (i = 0; i < li.length; i++) {
    a = li[i].getElementsByTagName("a")[0];
    txtValue = a.textContent || a.innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
}


function desactivar() {
    var ul, li, a, x
    ul = document.getElementById("lista");
    li = ul.getElementsByTagName('li');
  
    for (x = 0; x < li.length; x++) {
      li[x].classList.add('disabled')
      a= li[x].getElementsByTagName('a')
      a[1].style.display = "";
      a[0].style.display = "none";
      }
  }

function confirmar(){
  return confirm('Confirma la eliminacion del archivo.')

}