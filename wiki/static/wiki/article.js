$(document).ready(function(){

    // affichage du descriptif du logiciels (depuis l'application logiciel)
    urlpathname = window.location.pathname
    arraypath = urlpathname.split('/')
    if ((arraypath[1]=='logiciels')&&(arraypath.length==4)){
      url = 'http://127.0.0.1:8000/api/logiciel?libelle=A'  ;
      $.ajax({
         // headers: {'X-CSRFToken': csrftoken},
         url : url, // La ressource ciblée
         type : 'GET', // Le type de la requête HTTP.
         mode: 'same-origin',
         data : '',
         dataType : 'json',
         success : function(retour, statut){ // actions lorsque le résultat est reçu
           descriptif = retour[0]['descriptif']
           $("#retourPostAjax").text(retour[0]['descriptif'])

         },
         error : function(resultat, statut, erreur){
            console.log('appel Ajax error');
        },
        complete : function(resultat, statut){
        },
      });
    }
})
