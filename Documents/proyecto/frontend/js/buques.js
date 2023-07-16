const { createApp } = Vue;

// Crea una instancia de la aplicación Vue
createApp({
  data() {
    /* El código define una instancia de la aplicación Vue. Aquí se especifican los datos utilizados por la aplicación, incluyendo la lista de barcos, la URL del backend, indicadores de error y carga, así como los atributos para almacenar los valores del formulario de barco.
     */
    return {
      buques: [], // Almacena los buques obtenidos del backend
      // url:'http://localhost:5000/buques', // URL local
      url: "https://Ultrasea.pythonanywhere.com/buques", // URL del backend donde se encuentran los barcos
      error: false,
      cargando: true,
      // Atributos para el almacenar los valores del formulario
      id: 0,
      matricula: "",
      nombre: "",
      tipo: "",
      eslora: 0.00,
      tat: 0,
      imagen: "",
    };
  },
  methods: {
    fetchData(url) {
      /**El método fetchData realiza una solicitud HTTP utilizando la función fetch a la URL especificada. Luego, los datos de respuesta se convierten en formato JSON y se asignan al arreglo productos. Además, se actualiza la variable cargando para indicar que la carga de productos ha finalizado. En caso de producirse un error, se muestra en la consola y se establece la variable error en true.
       *
       */
      fetch(url) 
        .then((response) => response.json()) // Convierte la respuesta en formato JSON
        .then((data) => {
          // Asigna los datos de los barcos obtenidos al arreglo 'barcos'
          this.buques = data;
          this.cargando = false;
        })
        .catch((err) => {
          console.error(err);
          this.error = true;
        });
    },
    eliminar(buque) {
      /* El método eliminar toma un parámetro buque y construye la URL para eliminar ese buque en particular. Luego, realiza una solicitud fetch utilizando el método HTTP DELETE a la URL especificada. Después de eliminar el producto, la página se recarga para reflejar los cambios.
       */
      // Construye la URL para eliminar el buque especificado
      const url = this.url + "/" + buque;
      var options = {
        method: "DELETE", // Establece el método HTTP como DELETE
      };
      fetch(url, options)
        .then((res) => res.text()) // Convierte la respuesta en texto (or res.json())
        .then((res) => {
          location.reload(); // Recarga la página actual después de eliminar el buque
        });
    },
    grabar() {
      /* El método grabar se encarga de guardar los datos de un nuevo buque en el servidor. Primero, se crea un objeto buque con los datos ingresados en el formulario. Luego, se configuran las opciones para la solicitud fetch, incluyendo el cuerpo de la solicitud como una cadena JSON, el método HTTP como POST y el encabezado Content-Type como application/json. Después, se realiza la solicitud fetch a la URL especificada utilizando las opciones establecidas. Si la operación se realiza con éxito, se muestra un mensaje de éxito y se redirige al usuario a la página de productos. Si ocurre algún error, se muestra un mensaje de error.
       */
      // Crear un objeto 'buque' con los datos del formulario
      let buque = {
        matricula: this.matricula,
        nombre: this.nombre,
        tipo: this.tipo,
        eslora: this.eslora,
        tat: this.tat,
        imagen: this.imagen,
      };

      // Configurar las opciones para la solicitud fetch
      var options = {
        body: JSON.stringify(buque), // Convertir el objeto a una cadena JSON
        method: "POST", // Establecer el método HTTP como POST
        headers: { "Content-Type": "application/json" },
        redirect: "follow",
      };

      // Realizar una solicitud fetch para guardar el buque en el servidor
      fetch(this.url, options)
        .then(function () {
          alert("Registro grabado!");
          window.location.href = "../html/buques.html"; // Redirigir a la página de buques
        })
        .catch((err) => {
          console.error(err);
          alert("Error al Grabar.");
        });
    },
  },
  created() {
    this.fetchData(this.url);
  },
}).mount("#app");
