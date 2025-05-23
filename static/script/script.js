//Funcion para obtener la plantilla actual

function getCurrentTemplate() {
    var path = window.location.pathname;
    var templateNameWithParam = path.substring(1);
  
    // Utilizamos split() para dividir la cadena en partes utilizando "/"
    // Tomamos la primera parte que corresponde al nombre de la plantilla
    var templateName = templateNameWithParam.split("/")[0];
  
    return templateName;
}


//Obtener la plantilla actual HTML donde se encuentra el usuario
var currentTemplate = getCurrentTemplate();

//Validaciones para los campos de las plantillas HTML
if (currentTemplate === 'edit_user' || currentTemplate === 'create_user' || currentTemplate == 'registro') {

    var cedulaInput = document.getElementById('txtCedula');
    var nombreInput = document.getElementById('txtNombre');
    var apellidoInput = document.getElementById('txtApellido');
    var telefonoInput = document.getElementById('txtTelefono');


    // Funciones para validar los campos:

    cedulaInput.addEventListener('keypress', function(event) {
        var keyCode = event.keyCode || event.which;
        if (keyCode < 48 || keyCode > 57) {
            event.preventDefault();
    }
    });

    // Agregar un evento de escucha para el evento keypress en cada input
    nombreInput.addEventListener('keypress', function(event) {
        // Obtener el código de la tecla presionada
        var keyCode = event.keyCode || event.which;
        
        // Verificar si el código corresponde a una letra o espacio y cancelar el evento si no es así
        if ((keyCode < 65 || keyCode > 90) && (keyCode < 97 || keyCode > 122) && keyCode !== 32) {
            event.preventDefault();
        }
    });
        

    apellidoInput.addEventListener('keypress', function(event) {
    var keyCode = event.keyCode || event.which;
        if ((keyCode < 65 || keyCode > 90) && (keyCode < 97 || keyCode > 122) && keyCode !== 32) {
            event.preventDefault();
        }
    });

    telefonoInput.addEventListener('keypress', function(event) {

        var keyCode = event.keyCode || event.which;
        if (keyCode < 48 || keyCode > 57) {
            event.preventDefault();
        }
    });
}  
  
if (currentTemplate === 'create_nino') {

    var cedulaInput = document.getElementById('txtCedula');
    var nombreInput = document.getElementById('txtNombre');
    var apellidoInput = document.getElementById('txtApellido');
    var edadInput = document.getElementById('txtEdad');
    apellidoInput.addEventListener('keypress', function(event) {
    var keyCode = event.keyCode || event.which;
        if ((keyCode < 65 || keyCode > 90) && (keyCode < 97 || keyCode > 122) && keyCode !== 32) {
            event.preventDefault();
        }
    });

    telefonoInput.addEventListener('keypress', function(event) {

        var keyCode = event.keyCode || event.which;
        if (keyCode < 48 || keyCode > 57) {
            event.preventDefault();
        }
    });
}  
  
if (currentTemplate === 'create_nino') {

    var cedulaInput = document.getElementById('txtCedula');
    var nombreInput = document.getElementById('txtNombre');
    var apellidoInput = document.getElementById('txtApellido');
    var edadInput = document.getElementById('txtEdad');

    cedulaInput.addEventListener('keypress', function(event) {
        var keyCode = event.keyCode || event.which;
        if (keyCode < 48 || keyCode > 57) {
            event.preventDefault();
    }
    });
    cedulaInput.addEventListener('keypress', function(event) {
        var keyCode = event.keyCode || event.which;
        if (keyCode < 48 || keyCode > 57) {
            event.preventDefault();
    }
    });

    // Agregar un evento de escucha para el evento keypress en cada input
    nombreInput.addEventListener('keypress', function(event) {
        // Obtener el código de la tecla presionada
        var keyCode = event.keyCode || event.which;
        
        // Verificar si el código corresponde a una letra o espacio y cancelar el evento si no es así
        if ((keyCode < 65 || keyCode > 90) && (keyCode < 97 || keyCode > 122) && keyCode !== 32) {
            event.preventDefault();
        }
    });
        

    apellidoInput.addEventListener('keypress', function(event) {
    var keyCode = event.keyCode || event.which;
        if ((keyCode < 65 || keyCode > 90) && (keyCode < 97 || keyCode > 122) && keyCode !== 32) {
            event.preventDefault();
        }
    });

    edadInput.addEventListener('keypress', function(event) { 
        var keyCode = event.keyCode || event.which; 

        if (keyCode < 48 || keyCode > 57) { 
            event.preventDefault(); 
        } 
    });
}

if (currentTemplate === 'create_factura') {

    var cedulaInput = document.getElementById('txtCedula');
    var nombreInput = document.getElementById('txtNombre');
    var apellidoInput = document.getElementById('txtApellido');
    var cantidadInput = document.getElementById('txtCantidad');
    var precioInput = document.getElementById('txtPrecio');

    // Funciones para validar los campos:

    cedulaInput.addEventListener('keypress', function(event) {
        var keyCode = event.keyCode || event.which;
        if (keyCode < 48 || keyCode > 57) {
            event.preventDefault();
        }
    });

    // Agregar un evento de escucha para el evento keypress en cada input
    nombreInput.addEventListener('keypress', function(event) {
        // Obtener el código de la tecla presionada
        var keyCode = event.keyCode || event.which;
        
        // Verificar si el código corresponde a una letra o espacio y cancelar el evento si no es así
        if ((keyCode < 65 || keyCode > 90) && (keyCode < 97 || keyCode > 122) && keyCode !== 32) {
            event.preventDefault();
        }
    });
        

    apellidoInput.addEventListener('keypress', function(event) {
    var keyCode = event.keyCode || event.which;
        if ((keyCode < 65 || keyCode > 90) && (keyCode < 97 || keyCode > 122) && keyCode !== 32) {
            event.preventDefault();
        }
    });

    cantidadInput.addEventListener('keypress', function(event) {
        var keyCode = event.keyCode || event.which;
        if (keyCode < 48 || keyCode > 57) {
            event.preventDefault();
        }
    });

    precioInput.addEventListener('keypress', function(event) {
        var keyCode = event.keyCode || event.which;
        if (keyCode < 48 || keyCode > 57) {
            event.preventDefault();
        }
    });

    // Agregar un evento de escucha para el evento keypress en cada input
    nombreInput.addEventListener('keypress', function(event) {
        // Obtener el código de la tecla presionada
        var keyCode = event.keyCode || event.which;
        
        // Verificar si el código corresponde a una letra o espacio y cancelar el evento si no es así
        if ((keyCode < 65 || keyCode > 90) && (keyCode < 97 || keyCode > 122) && keyCode !== 32) {
            event.preventDefault();
        }
    });
        

    apellidoInput.addEventListener('keypress', function(event) {
    var keyCode = event.keyCode || event.which;
        if ((keyCode < 65 || keyCode > 90) && (keyCode < 97 || keyCode > 122) && keyCode !== 32) {
            event.preventDefault();
        }
    });

}

function calcularEdad() {
    // Obtener el valor de la fecha de nacimiento
    var fechaNacimiento = document.getElementById("txtFecha_Nac").value;
  
    // Calcular la fecha actual
    var fechaActual = new Date();
  
    // Calcular la diferencia en milisegundos entre la fecha actual y la fecha de nacimiento
    var diferencia = fechaActual - new Date(fechaNacimiento);
  
    // Convertir la diferencia en años
    var edad = Math.floor(diferencia / 31557600000); // aproximadamente la cantidad de milisegundos en un año
  
    // Asignar la edad calculada al campo "txtEdad"
    document.getElementById("txtEdad").value = edad;
}

// Funcion para realizar la busqueda en las tablas de las plantillas HTML
function searchTable() {

    const input = document.getElementById('searchInput');
    const filter = input.value.toUpperCase();
    const table = document.getElementById('myTable');
    const rows = table.getElementsByTagName('tr');
  
    for (let i = 0; i < rows.length; i++) {
      const cells = rows[i].getElementsByTagName('td');
      let found = false;
      
      // Aquí verificamos si la fila actual contiene el término de búsqueda en alguna celda <td>
      for (let j = 0; j < cells.length; j++) {
        const cell = cells[j];
        if (cell) {
          const textValue = cell.textContent || cell.innerText;
          if (textValue.toUpperCase().indexOf(filter) > -1) {
            found = true;
            break;
          }
        }
      }
      
      // Aquí controlamos la visibilidad de la fila para que las filas que se ocultan no sean las que contienen <th>
      if (rows[i].getElementsByTagName('th').length === 0) {
        if (found) {
          rows[i].style.display = '';
        } else {
          rows[i].style.display = 'none';
        }
      }
    }
}