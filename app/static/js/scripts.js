
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

    Guadalajara = ['Bachillerato','Derecho', 'Psicologia', 'Negocios Internacionales', 'Administracion', 'Mercadotecnia', 'Contaduria publica']
    Tlaquepaque= ['Bachillerato','Ingenieria en Computacion', 'Ingenieria en Electronica', 'Ingenieria Industrial','Ingenieria Civil']
    Zapopan = ['Bachillerato','Derecho', 'Gastronimia', 'Ingenieria Industrial','Quimica']
    var i
    universidad = document.getElementById("campus").value;
    selector = document.getElementById("carreras")
    padre = document.querySelector('#carreras')

    console.log(universidad)
    if(universidad == "Guadalajara"){
        removerHijos(padre);
        for(i=0;i<Guadalajara.length;i++){
            var option = document.createElement("option");
            option.value = Guadalajara[i];
            option.innerHTML= Guadalajara[i];
            selector.appendChild(option);
        }
    }
    else if(universidad == "Tlaquepaque"){
        removerHijos(padre);
        for(i=0;i<Tlaquepaque.length;i++){
            var option = document.createElement("option");
            option.value = Tlaquepaque[i];
            option.innerHTML= Tlaquepaque[i];
            selector.appendChild(option);
        }
    }else if(universidad == "Zapopan"){
        removerHijos(padre);
        for(i=0;i<Zapopan.length;i++){
            var option = document.createElement("option");
            option.value = Zapopan[i];
            option.innerHTML= Zapopan[i];
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
    matricula = document.getElementById("matricula").value
    password = document.getElementById("passwordA").value

    vMatricula = /^[0-9]{9,11}$/
    vPass = /^[a-zA-Z0-9]+$/
    error = 0;
    

    /* validacion usuario tamaño y caracteres correctos */
    if(matricula.length > 0){
        if(vMatricula.test(matricula) == false){
            document.getElementById("matricula").classList.add("error")
            document.getElementById("passwordA").setAttribute("disabled","")
            document.getElementById("aerrorMsg1").classList.remove("ocultar")
            error = 1;
        }else if(matricula.length < 9 || matricula.length > 11){
            document.getElementById("matricula").classList.add("error")
            document.getElementById("passwordA").setAttribute("disabled","")
            document.getElementById("aerrorMsg2").classList.remove("ocultar")
            error = 1;
        
        }else{
            document.getElementById("matricula").classList.remove("error")
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
    if(password.length > 0  && matricula.length >= 9 && matricula.length <= 11 && error == 0){

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
    vEmail = /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@conectados.edu.mx/
    vNum =  /^[0-9]{10}$/
    vMatricula = /^[0-9]{9,11}$/
    //elementos a revisar
    email = document.getElementById("email").value;
    password = document.getElementById("passwordR").value;
    matricula = document.getElementById("matriculaR").value;
    
    error=0;

    //Validaciones

    /**Matricula validacion campo vacio y validacion regex */
    if(matricula.length > 0 ){//si los campos no estan vacios
        if(vMatricula.test(matricula) == false){//si la validacion falla:
            n = document.getElementById("matriculaR")//elemento al que seleccionamos  para añadir la clase error
            n.classList.add("error")// se añade la clase error
            document.getElementById("email").setAttribute("disabled", "")// se añade el atributo disabled al elemento siguiente
            document.getElementById("errorMsg5").classList.remove("ocultar")// se remueve la clase ocultar para que el div error se muestre
            error=1;// bandera para los errores
        }else if(matricula.length < 9 || matricula.length > 11 ){// se revisa si la cantidad es diferente y se muestra el error si sobran o faltan caracteres
            n = document.getElementById("matriculaR")//elemento al que seleccionamos  para añadir la clase error
            n.classList.add("error")// se añade la clase error
            document.getElementById("email").setAttribute("disabled", "")// se añade el atributo disabled al elemento siguiente
            document.getElementById("errorMsg13").classList.remove("ocultar")// se remueve la clase ocultar para que el div error se muestre
            error=1;// bandera para los errores
        }else{
            n = document.getElementById("matriculaR")//elemento al que seleccionamos para remover la clase error
            n.classList.remove("error")//se remueve la clase error
            document.getElementById("email").removeAttribute("disabled")// se remueve el atributo disabled al elemento siguiente
            document.getElementById("errorMsg5").classList.add("ocultar")// se añade la clase ocultar para que el div error se muestre
            document.getElementById("errorMsg13").classList.add("ocultar")// se añade la clase ocultar para que el segundo div error  se muestre
            error=0;// bandera para los errores
        }
    }else{
        document.getElementById("email").setAttribute("disabled", "")//si el elemento a validar esta vacio se deshabilita el siguiente elemento
        error=1;// bandera para los errores
    }
    /**email validacion campo vacio y validacion regex */
    if(email.length > 0 && matricula.length > 0  && error == 0){//si los campos no estan vacios
        if(vEmail.test(email) == false){//si la validacion falla:
            n = document.getElementById("email")//elemento al que seleccionamos  para añadir la clase error
            n.classList.add("error")// se añade la clase error
            document.getElementById("passwordR").setAttribute("disabled", "")// se añade el atributo disabled al elemento siguiente
            document.getElementById("errorMsg4").classList.remove("ocultar")// se remueve la clase ocultar para que el div error se muestre
            error=1;// bandera para los errores
        }else{
            n = document.getElementById("email")//elemento al que seleccionamos para remover la clase error
            n.classList.remove("error")//se remueve la clase error
            document.getElementById("passwordR").removeAttribute("disabled")// se remueve el atributo disabled al elemento siguiente
            document.getElementById("errorMsg4").classList.add("ocultar")// se añade la clase ocultar para queel div error se muestre
            error=0;// bandera para los errores
        }
    }else{
        document.getElementById("passwordR").setAttribute("disabled", "")//si el elemento a validar esta vacio se deshabilita el siguiente
        error=1;// bandera para los errores
    }
    /**Contraseña validacion campo vacio y validacion regex */
    if(matricula.length > 0 && email.length > 0 && password.length > 0 && error == 0){//si los campos no estan vacios
        if(vPass.test(password) == false){//si la validacion falla:
            n = document.getElementById("passwordR")//elemento al que seleccionamos  para añadir la clase error
            n.classList.add("error")// se añade la clase error
            document.getElementById("registrar").setAttribute("disabled", "")// se añade el atributo disabled al elemento siguiente
            document.getElementById("errorMsg11").classList.remove("ocultar")// se remueve la clase ocultar para que el div error se muestre
            error=1;// bandera para los errores
        }else if(password.length < 8 || password.length > 20 ){// se revisa si la cantidad es diferente y se muestra el error si sobran o faltan caracteres
            n = document.getElementById("passwordR")//elemento al que seleccionamos  para añadir la clase error
            n.classList.add("error")// se añade la clase error
            document.getElementById("registrar").setAttribute("disabled", "")// se añade el atributo disabled al elemento siguiente
            document.getElementById("errorMsg10").classList.remove("ocultar")// se remueve la clase ocultar para que el div error se muestre
            error=1;// bandera para los errores
        }else{
            n = document.getElementById("passwordR")//elemento al que seleccionamos para remover la clase error
            n.classList.remove("error")//se remueve la clase error
            document.getElementById("registrar").removeAttribute("disabled")// se remueve el atributo disabled al elemento siguiente
            document.getElementById("errorMsg11").classList.add("ocultar")// se añade la clase ocultar para que el div error se muestre
            document.getElementById("errorMsg10").classList.add("ocultar")// se añade la clase ocultar para que el segundo div error  se muestre
            error=0;// bandera para los errores
        }
    }else{
        document.getElementById("registrar").setAttribute("disabled", "")//si el elemento a validar esta vacio se deshabilita el siguiente elemento
        error=1;// bandera para los errores
    }
}



function contraValidacion(){
    password=document.getElementById("actual").value
    nueva = document.getElementById("nueva").value
    repetir = document.getElementById("repetir").value
    
    vPass = /^[a-zA-Z0-9]+$/

    //Validacion de contraseña actual
    if(password.length > 0){

        if(vPass.test(password) == false){
            document.getElementById("actual").classList.add("error")
            document.getElementById("nueva").setAttribute("disabled","")
            document.getElementById("errorMsg1").classList.remove("ocultar")
            document.getElementById("errorMsg2").classList.add("ocultar")
            error = 1;
        }else if(password.length < 8 || password.length > 20){
            document.getElementById("actual").classList.add("error")
            document.getElementById("nueva").setAttribute("disabled","")
            document.getElementById("errorMsg2").classList.remove("ocultar")
            document.getElementById("errorMsg1").classList.add("ocultar")
            error = 1;
        
        }else{
            document.getElementById("actual").classList.remove("error")
            document.getElementById("nueva").removeAttribute("disabled","")
            document.getElementById("errorMsg1").classList.add("ocultar")
            document.getElementById("errorMsg2").classList.add("ocultar")
            error = 0;
        }


    }else{
        document.getElementById("nueva").setAttribute("disabled","")
        error = 1;
    }

    //Validacion de contraseña nueva
    if(password.length > 0 && nueva.length > 0 && error == 0){

        if(vPass.test(nueva) == false){
            document.getElementById("nueva").classList.add("error")
            document.getElementById("repetir").setAttribute("disabled","")
            document.getElementById("errorMsg3").classList.remove("ocultar")
            document.getElementById("errorMsg4").classList.add("ocultar")
            document.getElementById("errorMsg8").classList.add("ocultar")
            error = 1;
        }else if(nueva.length < 8 || nueva.length > 20){
            document.getElementById("nueva").classList.add("error")
            document.getElementById("repetir").setAttribute("disabled","")
            document.getElementById("errorMsg4").classList.remove("ocultar")
            document.getElementById("errorMsg3").classList.add("ocultar")
            document.getElementById("errorMsg8").classList.add("ocultar")
            error = 1;
        
        }else if(nueva == password){
            document.getElementById("nueva").classList.add("error")
            document.getElementById("repetir").setAttribute("disabled","")
            document.getElementById("errorMsg4").classList.add("ocultar")
            document.getElementById("errorMsg3").classList.add("ocultar")
            document.getElementById("errorMsg8").classList.remove("ocultar")
            error = 1;
        }else{
            document.getElementById("nueva").classList.remove("error")
            document.getElementById("repetir").removeAttribute("disabled","")
            document.getElementById("errorMsg3").classList.add("ocultar")
            document.getElementById("errorMsg4").classList.add("ocultar")
            document.getElementById("errorMsg8").classList.add("ocultar")
            error = 0;
        }


    }else{
        document.getElementById("repetir").setAttribute("disabled","")
        error = 1;
    }

    //Validacion contraseña repetida
    if(repetir.length > 0 && password.length > 0 && nueva.length > 0 && error == 0){

        if(vPass.test(repetir) == false){
            document.getElementById("repetir").classList.add("error")
            document.getElementById("cambiar").setAttribute("disabled","")
            document.getElementById("errorMsg5").classList.remove("ocultar")
            document.getElementById("errorMsg6").classList.add("ocultar")
            document.getElementById("errorMsg7").classList.add("ocultar")
            error = 1;
        }else if(repetir.length < 8 || repetir.length > 20){
            document.getElementById("repetir").classList.add("error")
            document.getElementById("cambiar").setAttribute("disabled","")
            document.getElementById("errorMsg6").classList.remove("ocultar")
            document.getElementById("errorMsg5").classList.add("ocultar")
            document.getElementById("errorMsg7").classList.add("ocultar")
            error = 1;
        
        }else if(nueva != repetir){
            document.getElementById("repetir").classList.add("error")
            document.getElementById("cambiar").setAttribute("disabled","")
            document.getElementById("errorMsg6").classList.add("ocultar")
            document.getElementById("errorMsg5").classList.add("ocultar")
            document.getElementById("errorMsg7").classList.remove("ocultar")
            error = 1;
        }else{
            document.getElementById("repetir").classList.remove("error")
            document.getElementById("cambiar").removeAttribute("disabled","")
            document.getElementById("errorMsg5").classList.add("ocultar")
            document.getElementById("errorMsg6").classList.add("ocultar")
            document.getElementById("errorMsg7").classList.add("ocultar")
            error = 0;
        }


    }else{
        document.getElementById("cambiar").setAttribute("disabled","")
        error = 1;
    }


}