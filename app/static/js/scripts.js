
function mostrarInicio(){


    var seleccion = document.getElementById("plantel").value;	
    escuelas = document.querySelectorAll('.bloqueCampus');
    var i

    console.log(parseInt(seleccion));
    console.log(escuelas);
    if(parseInt(seleccion) == 0){
        for (i = 0; i < escuelas.length; i++){
                escuelas[i].classList.remove("ocultar");
        }
    }else{
        for (i = 0; i < escuelas.length; i++){

            if(i+1 == parseInt(seleccion)  ){
                escuelas[i].classList.remove("ocultar");
            }
            else{
                escuelas[i].classList.add("ocultar");
            }
        }
    }
    
    

    // if(seleccion == "9"){

    //     document.getElementById("Tlajomulco").classList.remove("ocultar")
    //     document.getElementById("Rio Nilo").classList.remove("ocultar")
    //     document.getElementById("Lazaro Cardenas").classList.remove("ocultar")
    //     document.getElementById("Campus").classList.remove("ocultar")
    //     document.getElementById("Americas").classList.remove("ocultar")
    //     document.getElementById("Zapopan").classList.remove("ocultar")
    //     document.getElementById("Pedro Moreno").classList.remove("ocultar")
    //     document.getElementById("Olimpica").classList.remove("ocultar")
    // }else if(seleccion == "1"){

    //     document.getElementById("Tlajomulco").classList.remove("ocultar")
    //     document.getElementById("Rio Nilo").classList.add("ocultar")
    //     document.getElementById("Lazaro Cardenas").classList.add("ocultar")
    //     document.getElementById("Campus").classList.add("ocultar")
    //     document.getElementById("Americas").classList.add("ocultar")
    //     document.getElementById("Zapopan").classList.add("ocultar")
    //     document.getElementById("Pedro Moreno").classList.add("ocultar")
    //     document.getElementById("Olimpica").classList.add("ocultar")
    // }else if(seleccion == "2"){

    //     document.getElementById("Tlajomulco").classList.add("ocultar")
    //     document.getElementById("Rio Nilo").classList.remove("ocultar")
    //     document.getElementById("Lazaro Cardenas").classList.add("ocultar")
    //     document.getElementById("Campus").classList.add("ocultar")
    //     document.getElementById("Americas").classList.add("ocultar")
    //     document.getElementById("Zapopan").classList.add("ocultar")
    //     document.getElementById("Pedro Moreno").classList.add("ocultar")
    //     document.getElementById("Olimpica").classList.add("ocultar")
    // }else 
}

function logSeleccion(valor){

    console.log(valor)
    valor1 = document.getElementById("btn1").value;
    valor2 = document.getElementById("btn2").value;
    boton1 = document.getElementById("btn1");
    boton2 = document.getElementById("btn2");

    if(valor == "0"){
        boton1.classList.add('btn-primary');
        boton1.classList.remove('btn-light');
        boton2.classList.remove('btn-primary');
        boton2.classList.add('btn-light');
        document.getElementById('acceso').classList.remove('ocultar');
        document.getElementById('registro').classList.add('ocultar');

    }else if(valor == "1"){
        boton2.classList.add('btn-primary');
        boton2.classList.remove('btn-light');
        boton1.classList.remove('btn-primary');
        boton1.classList.add('btn-light');
        document.getElementById('registro').classList.remove('ocultar');
        document.getElementById('acceso').classList.add('ocultar');
    }

}

function selCarreras(){

    tlajomulco = ['Derecho', 'Psicologia', 'Negocios Internacionales', 'Administracion', 'Mercadotecnia', 'Contaduria publica']
    rionilo = ['Derecho', 'Administracion', 'Negocios Internacionales','Mercadotecnia', 'Contaduria publica']
    lazarocardenas = ['Derecho', 'Carrera de abogado']
    campus = ['Nutricion', 'Cultura Fisica y deporte', 'Psicologia', 'Enfermeria','Quimico farmaceutico biologo','Cirujano Dentista', 'Negocios Internacionales','Administracion', 'Mercadotecnia', 'Contaduria publica','Gestion de recursos humanos']
    americas = ['Trabajo Social', 'Carrera de abogado', 'Derecho', 'Gastronimia', 'Diseño de modas', 'Diseño para la comunicacion grafica','Diseño de interiores','Arquitectura', 'Negocios Internacionales', 'Administracion', 'Mercadotecnia', 'Contaduria publica' ]
    zapopan = ['Carrera de abogado', 'Derecho', 'Psicologia', 'Negocios Internacionales','Administracion', 'Mercadotecnia', 'Contaduria publica', 'Gestion recursos humanos']
    pedromoreno = ['Trabajo social', 'Derecho', 'Gastronomia', 'Negocios Internacionales', 'Administracion', 'Mercadotecnia', 'Contaduria publica']
    olimpica = ['Comunicacion y Electronica', 'Industrial', 'Computacion', 'Civil']
    var i
    universidad = document.getElementById("campus").value;
    selector = document.getElementById("carreras")
    padre = document.querySelector('#carreras')

    console.log(universidad)
    if(universidad == "Tlajomulco"){
        removerHijos(padre);
        for(i=0;i<tlajomulco.length;i++){
            var option = document.createElement("option");
            option.value = tlajomulco[i];
            option.innerHTML= tlajomulco[i];
            selector.appendChild(option);
        }
    }
    else if(universidad == "Rio Nilo"){
        removerHijos(padre);
        for(i=0;i<rionilo.length;i++){
            var option = document.createElement("option");
            option.value = rionilo[i];
            option.innerHTML= rionilo[i];
            selector.appendChild(option);
        }
    }else if(universidad == "Lazaro Cardenas"){
        removerHijos(padre);
        for(i=0;i<lazarocardenas.length;i++){
            var option = document.createElement("option");
            option.value = lazarocardenas[i];
            option.innerHTML= lazarocardenas[i];
            selector.appendChild(option);
        }
    }else if(universidad == "Campus"){
        removerHijos(padre);
        for(i=0;i<campus.length;i++){
            var option = document.createElement("option");
            option.value = campus[i];
            option.innerHTML= campus[i];
            selector.appendChild(option);
        }
        
    }else if(universidad == "Americas"){
        removerHijos(padre);
        for(i=0;i<americas.length;i++){
            var option = document.createElement("option");
            option.value = americas[i];
            option.innerHTML= americas[i];
            selector.appendChild(option);
        }
        
    }else if(universidad == "Zapopan"){
        removerHijos(padre);
        for(i=0;i<zapopan.length;i++){
            var option = document.createElement("option");
            option.value = zapopan[i];
            option.innerHTML= zapopan[i];
            selector.appendChild(option);
        }
        
    }else if(universidad == "Pedro Moreno"){
        removerHijos(padre);
        for(i=0;i<pedromoreno.length;i++){
            var option = document.createElement("option");
            option.value = pedromoreno[i];
            option.innerHTML= pedromoreno[i];
            selector.appendChild(option);
        }
        
    }else if(universidad == "Olimpica"){
        removerHijos(padre);
        for(i=0;i<olimpica.length;i++){
            var option = document.createElement("option");
            option.value = olimpica[i];
            option.innerHTML= olimpica[i];
            selector.appendChild(option);
        }
    }else{
        removerHijos(padre);
        var option = document.createElement("option");
            option.value = "0";
            option.innerHTML= "--Seleccionar--";
            selector.appendChild(option);

    }
            
    
    
    function removerHijos(padre){
        while(padre.firstChild){
            padre.removeChild(padre.firstChild);
        }
    }

}

function validacionAcceso(){
    usuario = document.getElementById("usuarioA").value
    password = document.getElementById("passwordA").value

    vAcceso = /^[a-zA-Z]+$/
    vPass = /^[a-zA-Z0-9]+$/
    vNumero = /^[0-9]+$/
    error = 0;
    

    /* validacion usuario tamaño y caracteres correctos */
    if(usuario.length > 0){
        if(vAcceso.test(usuario) == false){
            document.getElementById("usuarioA").classList.add("error")
            document.getElementById("passwordA").setAttribute("disabled","")
            document.getElementById("aerrorMsg1").classList.remove("ocultar")
            error = 1;
        }else if(usuario.length < 6 || usuario.length > 10){
            document.getElementById("usuarioA").classList.add("error")
            document.getElementById("passwordA").setAttribute("disabled","")
            document.getElementById("aerrorMsg2").classList.remove("ocultar")
            error = 1;
        
        }else{
            document.getElementById("usuarioA").classList.remove("error")
            document.getElementById("passwordA").removeAttribute("disabled")
            document.getElementById("aerrorMsg2").classList.add("ocultar")
            document.getElementById("aerrorMsg1").classList.add("ocultar")
            error = 0;
        }
        
    }else{
        document.getElementById("passwordA").setAttribute("disabled","")
        
        error = 1;
    }

    /* valiadcion contraseña tamaño y caracteres correctos */
    if(password.length > 0  && usuario.length >= 6 && usuario.length <= 10 && error == 0){

        if(vPass.test(password) == false){
            document.getElementById("passwordA").classList.add("error")
            document.getElementById("acceder").setAttribute("disabled","")
            document.getElementById("aerrorMsg3").classList.remove("ocultar")
            error = 1;
        }else if(password.length < 8){
            document.getElementById("passwordA").classList.add("error")
            document.getElementById("acceder").setAttribute("disabled","")
            document.getElementById("aerrorMsg4").classList.remove("ocultar")
            error = 1;
        }else{
            document.getElementById("passwordA").classList.remove("error")
            document.getElementById("acceder").removeAttribute("disabled","")
            document.getElementById("aerrorMsg3").classList.add("ocultar")
            error = 0;
        }
        
    
    }else{
        document.getElementById("acceder").setAttribute("disabled","")
        error = 1;
    }


}

function validacionRegistro(){

    //expresiones regulares
    vNom = /^([A-Za-z]*([\s][A-Za-z]+)*)$/
    vPass = /^[a-zA-Z0-9]+$/
    vUser = /^[a-zA-Z]+$/
    vEmail = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/
    vNum =  /^[0-9]{10}$/
    vMatricula = /^[0-9]{9,11}$/
    //elementos a revisar
    nombre = document.getElementById("nombre").value;
    apellido1 = document.getElementById("apellido1").value;
    apellido2 = document.getElementById("apellido2").value;
    usuario = document.getElementById("usuarioR").value;
    password = document.getElementById("passwordR").value;
    email = document.getElementById("email").value;
    matricula = document.getElementById("matricula").value;
    telefono = document.getElementById("telefono").value;
    campus = document.getElementById("campus").value;
    carrera = document.getElementById("carreras").value;
    
    error=0;

    //Validaciones

    /**Nombre validacion campo vacio y validacion regex */
    if(nombre.length > 0){//si el campo no esta vacio
        if(vNom.test(nombre) == false){//si la validacion falla:
            n = document.getElementById("nombre") //elemento al que seleccionamos  para añadir la clase error
            n.classList.add("error")// se añade la clase error
            document.getElementById("apellido1").setAttribute("disabled", "")// se añade el atributo disabled al elemento siguiente
            document.getElementById("errorMsg1").classList.remove("ocultar")// se remueve la clase ocultar para que el div error se muestre
            error=1// bandera para los errores
        }else{//si la validacion acierta: 
            n = document.getElementById("nombre")//elemento al que seleccionamos para remover la clase error
            n.classList.remove("error")//se remueve la clase error
            document.getElementById("apellido1").removeAttribute("disabled")// se remueve el atributo disabled al elemento siguiente
            document.getElementById("errorMsg1").classList.add("ocultar")// se añade la clase ocultar para queel div error se muestre
            error=0//bandera para los errores
        }
        
    }else{
        document.getElementById("apellido1").setAttribute("disabled", "")//si el elemento a validar esta vacio se deshabilita el siguiente
        error=1;//bandera para los errores
    }
    /**Apellido1 validacion campo vacio y validacion regex */
    if(apellido1.length > 0 && nombre.length > 0 && error == 0){//si los campos no estan vacios
        if(vNom.test(apellido1) == false){//si la validacion falla:
            n = document.getElementById("apellido1") //elemento al que seleccionamos  para añadir la clase error
            n.classList.add("error")// se añade la clase error
            document.getElementById("apellido2").setAttribute("disabled", "")// se añade el atributo disabled al elemento siguiente
            document.getElementById("errorMsg2").classList.remove("ocultar")// se remueve la clase ocultar para que el div error se muestre
            error=1;// bandera para los errores
            
        }else{
            n = document.getElementById("apellido1")//elemento al que seleccionamos para remover la clase error
            n.classList.remove("error")//se remueve la clase error
            document.getElementById("apellido2").removeAttribute("disabled")// se remueve el atributo disabled al elemento siguiente
            document.getElementById("errorMsg2").classList.add("ocultar")// se añade la clase ocultar para queel div error se muestre
            error=0;// bandera para los errores
        }
    }else{
        document.getElementById("apellido2").setAttribute("disabled", "")//si el elemento a validar esta vacio se deshabilita el siguiente
        error=1;// bandera para los errores
    }
    /**Apellido2 validacion campo vacio y validacion regex */
    if(apellido2.length > 0 && nombre.length > 0 && apellido1.length > 0 && error == 0){//si los campos no estan vacios
        if(vNom.test(apellido2) == false){//si la validacion falla:
            n = document.getElementById("apellido2")//elemento al que seleccionamos  para añadir la clase error
            n.classList.add("error")// se añade la clase error
            document.getElementById("usuarioR").setAttribute("disabled", "")// se añade el atributo disabled al elemento siguiente
            document.getElementById("errorMsg3").classList.remove("ocultar")// se remueve la clase ocultar para que el div error se muestre
            error=1;// bandera para los errores
            
        }else{
            n = document.getElementById("apellido2")//elemento al que seleccionamos para remover la clase error
            n.classList.remove("error")//se remueve la clase error
            document.getElementById("usuarioR").removeAttribute("disabled")// se remueve el atributo disabled al elemento siguiente
            document.getElementById("errorMsg3").classList.add("ocultar")// se añade la clase ocultar para queel div error se muestre
            error=0;// bandera para los errores
        }
    }else{
        document.getElementById("usuarioR").setAttribute("disabled", "")//si el elemento a validar esta vacio se deshabilita el siguiente
        error=1;// bandera para los errores
    }
    /**Usuario validacion campo vacio y validacion regex */
    if(usuario.length > 0 && apellido1.length > 0 && apellido2.length > 0 && nombre.length > 0 && error == 0){//si los campos no estan vacios
        if(vUser.test(usuario) == false){//si la validacion falla:
            n = document.getElementById("usuarioR")//elemento al que seleccionamos  para añadir la clase error
            n.classList.add("error")// se añade la clase error
            document.getElementById("passwordR").setAttribute("disabled", "")// se añade el atributo disabled al elemento siguiente
            document.getElementById("errorMsg4").classList.remove("ocultar")// se remueve la clase ocultar para que el div error se muestre
            error=1;// bandera para los errores
        }else if(usuario.length < 6 || usuario.length > 10){// se revisa si la cantidad es diferente y se muestra el error si sobran o faltan caracteres
            n = document.getElementById("usuarioR")//elemento al que seleccionamos  para añadir la clase error
            n.classList.add("error")// se añade la clase error
            document.getElementById("passwordR").setAttribute("disabled", "")// se añade el atributo disabled al elemento siguiente
            document.getElementById("errorMsg9").classList.remove("ocultar")// se remueve la clase ocultar para que el div error se muestre
            error=1;// bandera para los errores
        }else{
            n = document.getElementById("usuarioR")//elemento al que seleccionamos para remover la clase error
            n.classList.remove("error")//se remueve la clase error
            document.getElementById("passwordR").removeAttribute("disabled")// se remueve el atributo disabled al elemento siguiente
            document.getElementById("errorMsg4").classList.add("ocultar")// se añade la clase ocultar para queel div error se muestre
            document.getElementById("errorMsg9").classList.add("ocultar")// se remueve la clase ocultar para que el segundo div error se muestre
            error=0;// bandera para los errores
        }
    }else{
        document.getElementById("passwordR").setAttribute("disabled", "")//si el elemento a validar esta vacio se deshabilita el siguiente
        error=1;// bandera para los errores
    }
    /**Contraseña validacion campo vacio y validacion regex */
    if(password.length > 0 && usuario.length > 0 && apellido1.length > 0 && apellido2.length > 0 && nombre.length > 0 && error == 0){//si los campos no estan vacios
        if(vPass.test(password) == false){//si la validacion falla:
            n = document.getElementById("passwordR")//elemento al que seleccionamos  para añadir la clase error
            n.classList.add("error")// se añade la clase error
            document.getElementById("email").setAttribute("disabled", "")// se añade el atributo disabled al elemento siguiente
            document.getElementById("errorMsg11").classList.remove("ocultar")// se remueve la clase ocultar para que el div error se muestre
            error=1;// bandera para los errores
        }else if(password.length != 8){// se revisa si la cantidad es diferente y se muestra el error si sobran o faltan caracteres
            n = document.getElementById("passwordR")//elemento al que seleccionamos  para añadir la clase error
            n.classList.add("error")// se añade la clase error
            document.getElementById("email").setAttribute("disabled", "")// se añade el atributo disabled al elemento siguiente
            document.getElementById("errorMsg10").classList.remove("ocultar")// se remueve la clase ocultar para que el div error se muestre
            error=1;// bandera para los errores
        }else{
            n = document.getElementById("passwordR")//elemento al que seleccionamos para remover la clase error
            n.classList.remove("error")//se remueve la clase error
            document.getElementById("email").removeAttribute("disabled")// se remueve el atributo disabled al elemento siguiente
            document.getElementById("errorMsg11").classList.add("ocultar")// se añade la clase ocultar para que el div error se muestre
            document.getElementById("errorMsg10").classList.add("ocultar")// se añade la clase ocultar para que el segundo div error  se muestre
            error=0;// bandera para los errores
        }
    }else{
        document.getElementById("email").setAttribute("disabled", "")//si el elemento a validar esta vacio se deshabilita el siguiente elemento
        error=1;// bandera para los errores
    }
    /**email validacion campo vacio y validacion regex */
    if(email.length > 0 && password.length > 0 && usuario.length > 0 && apellido1.length > 0 && apellido2.length > 0 && nombre.length > 0 && error == 0){//si los campos no estan vacios
        if(vEmail.test(email) == false){//si la validacion falla:
            n = document.getElementById("email")//elemento al que seleccionamos  para añadir la clase error
            n.classList.add("error")// se añade la clase error
            document.getElementById("matricula").setAttribute("disabled", "")// se añade el atributo disabled al elemento siguiente
            document.getElementById("errorMsg12").classList.remove("ocultar")// se remueve la clase ocultar para que el div error se muestre
            error=1;// bandera para los errores
        }else{
            n = document.getElementById("email")//elemento al que seleccionamos para remover la clase error
            n.classList.remove("error")//se remueve la clase error
            document.getElementById("matricula").removeAttribute("disabled")// se remueve el atributo disabled al elemento siguiente
            document.getElementById("errorMsg12").classList.add("ocultar")// se añade la clase ocultar para que el div error se muestre
            error=0;// bandera para los errores
        }
    }else{
        document.getElementById("matricula").setAttribute("disabled", "")//si el elemento a validar esta vacio se deshabilita el siguiente elemento
        error=1;// bandera para los errores
    }
    /**matricula validacion campo vacio y validacion regex */
    if(matricula.length > 0 && email.length > 0 && usuario.length > 0 && apellido1.length > 0 && apellido2.length > 0 && nombre.length > 0 && error == 0){//si los campos no estan vacios
        if(vMatricula.test(matricula) == false){//si la validacion falla:
            n = document.getElementById("matricula")//elemento al que seleccionamos  para añadir la clase error
            n.classList.add("error")// se añade la clase error
            document.getElementById("telefono").setAttribute("disabled", "")// se añade el atributo disabled al elemento siguiente
            document.getElementById("errorMsg5").classList.remove("ocultar")// se remueve la clase ocultar para que el div error se muestre
            error=1;// bandera para los errores
        }else if(matricula.length < 9 || matricula.length > 11 ){// se revisa si la cantidad es diferente y se muestra el error si sobran o faltan caracteres
            n = document.getElementById("matricula")//elemento al que seleccionamos  para añadir la clase error
            n.classList.add("error")// se añade la clase error
            document.getElementById("telefono").setAttribute("disabled", "")// se añade el atributo disabled al elemento siguiente
            document.getElementById("errorMsg13").classList.remove("ocultar")// se remueve la clase ocultar para que el div error se muestre
            error=1;// bandera para los errores
        }else{
            n = document.getElementById("matricula")//elemento al que seleccionamos para remover la clase error
            n.classList.remove("error")//se remueve la clase error
            document.getElementById("telefono").removeAttribute("disabled")// se remueve el atributo disabled al elemento siguiente
            document.getElementById("errorMsg5").classList.add("ocultar")// se añade la clase ocultar para que el div error se muestre
            document.getElementById("errorMsg13").classList.add("ocultar")// se añade la clase ocultar para que el segundo div error  se muestre
            error=0;// bandera para los errores
        }
    }else{
        document.getElementById("telefono").setAttribute("disabled", "")//si el elemento a validar esta vacio se deshabilita el siguiente elemento
        error=1;// bandera para los errores
    }

    /**telefono validacion campo vacio y validacion regex */
    if(telefono.length > 0 && matricula.length > 0 && email.length > 0 && usuario.length > 0 && apellido1.length > 0 && apellido2.length > 0 && nombre.length > 0 && error == 0){//si los campos no estan vacios
        if(vNum.test(telefono) == false){//si la validacion falla:
            n = document.getElementById("campus")//elemento al que seleccionamos  para añadir la clase error
            n.classList.add("error")// se añade la clase error
            document.getElementById("campus").setAttribute("disabled", "")// se añade el atributo disabled al elemento siguiente
            document.getElementById("errorMsg6").classList.remove("ocultar")// se remueve la clase ocultar para que el div error se muestre
            error=1;// bandera para los errores
        }else if(password.length != 8){// se revisa si la cantidad es diferente y se muestra el error si sobran o faltan caracteres
            n = document.getElementById("campus")//elemento al que seleccionamos  para añadir la clase error
            n.classList.add("error")// se añade la clase error
            document.getElementById("campus").setAttribute("disabled", "")// se añade el atributo disabled al elemento siguiente
            document.getElementById("errorMsg14").classList.remove("ocultar")// se remueve la clase ocultar para que el div error se muestre
            error=1;// bandera para los errores
        }else{
            n = document.getElementById("campus")//elemento al que seleccionamos para remover la clase error
            n.classList.remove("error")//se remueve la clase error
            document.getElementById("campus").removeAttribute("disabled")// se remueve el atributo disabled al elemento siguiente
            document.getElementById("errorMsg6").classList.add("ocultar")// se añade la clase ocultar para que el div error se muestre
            document.getElementById("errorMsg14").classList.add("ocultar")// se añade la clase ocultar para que el segundo div error  se muestre
            error=0;// bandera para los errores
        }
    }else{
        document.getElementById("campus").setAttribute("disabled", "")//si el elemento a validar esta vacio se deshabilita el siguiente elemento
        error=1;// bandera para los errores
    }
    /* campus validacion campo vacio */
    if(campus.length > 0 && matricula.length > 0 && email.length > 0 && usuario.length > 0 && apellido1.length > 0 && apellido2.length > 0 && nombre.length > 0 && error == 0){//si los campos no estan vacios
            n = document.getElementById("carreras")//elemento al que seleccionamos para remover la clase error
            n.classList.remove("error")//se remueve la clase error
            document.getElementById("carreras").removeAttribute("disabled")// se remueve el atributo disabled al elemento siguiente
            document.getElementById("errorMsg7").classList.add("ocultar")// se añade la clase ocultar para que el div error se muestre
            error=0;// bandera para los errores
    }else{
        document.getElementById("carreras").setAttribute("disabled", "")//si el elemento a validar esta vacio se deshabilita el siguiente elemento
        error=1;// bandera para los errores
    }
    /* carrera validacion campo vacio */
    if(campus.length > 0 && telefono.length > 0 && matricula.length > 0 && email.length > 0 && usuario.length > 0 && apellido1.length > 0 && apellido2.length > 0 && nombre.length > 0 && error == 0){//si los campos no estan vacios
        n = document.getElementById("registrar")//elemento al que seleccionamos para remover la clase error
        n.classList.remove("error")//se remueve la clase error
        document.getElementById("registrar").removeAttribute("disabled")// se remueve el atributo disabled al elemento siguiente
        document.getElementById("errorMsg8").classList.add("ocultar")// se añade la clase ocultar para que el div error se muestre
        error=0;// bandera para los errores
}else{
    document.getElementById("registrar").setAttribute("disabled", "")//si el elemento a validar esta vacio se deshabilita el siguiente elemento
    error=1;// bandera para los errores
}
}