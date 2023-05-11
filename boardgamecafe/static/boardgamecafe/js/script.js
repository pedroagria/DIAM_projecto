// PARA IMAGEM NO FORM
function readImgURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#boardgame_image')
                .attr('src', e.target.result)
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// FUNCAO A FAZER PARA O SEARCH
// function filterBoardGames(boardgames, name, players, age, time){
//     // CREATE LIST OF BOARDGAMES
//     for(var i = 0; i < boardgames.length; i++){
//        if(!#name.empty()){
//            if(!boardgames[i].contains(name)){
//                continue;
//            }
//        }
//        if(!#players.empty()){
//            if(boardgames[i].min_players > players || boardgames[i].max_player < players){
//                continue;
//            }
//        }
//        if(!#age.empty()){
//            if(boardgames[i].min_age > age){
//                continue;
//            }
//        }
//        if(!#time.empty()){
//            if(boardgames[i].min_time > time){
//                continue;
//            }
//        }
//        //ADD BOARDGAME TO LIST
//     }
//     // RETURN LIST
// }