// FOR IMAGE IN ADD/EDIT GAME FORM
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

// FOR GAME FILTERING IN LIST OF GAMES
function filterBoardGames(boardgames, pageIndex){
    var parsed_boardgames = JSON.parse(boardgames);
    var name = document.getElementById('name').value.toUpperCase();
    var hasName = !(name == null || name == "");
    var players = document.getElementById('players').value;
    var hasPlayers = !(players == null || players == "");
    var age = document.getElementById('age').value;
    var hasAge = !(age == null || age == "");
    var time = document.getElementById('time').value;
    var hasTime = !(time == null || time == "");
    var filteredBoardGames = [];
    for(var i = 0; i < parsed_boardgames.length; i++){
        if(hasName){
            if(!(parsed_boardgames[i].name.toUpperCase().indexOf(name) > -1)){
               continue;
           }
        }
       if(hasPlayers){
           if(parseInt(parsed_boardgames[i].min_players) > parseInt(players) || parseInt(parsed_boardgames[i].max_players) < parseInt(players)){
               continue;
           }
       }
       if(hasAge){
           if(parseInt(parsed_boardgames[i].min_age) > parseInt(age)){
               continue;
           }
       }
       if(hasTime){
           if(parseInt(parsed_boardgames[i].min_playing_time) > parseInt(time)){
               continue;
           }
       }
       filteredBoardGames.push(parsed_boardgames[i]);
    }
    constructListPage(filteredBoardGames, pageIndex);
}

// FOR SHOWING CORRECT GAMES IN LIST
function constructListPage(boardgames, pageIndex){
    var grid = document.getElementById('boardgames_grid');
    var divs = grid.getElementsByTagName('div');
    var counter = 0;
    for(var i = 0; i < 9; i++){
        var boardgame_div = divs[i];
        var boardgame_img = boardgame_div.getElementsByTagName('img')[0];
        var boardgame_name = boardgame_div.getElementsByTagName('h3')[0];
        var current_id = (pageIndex - 1) * 9 + i;
        if(current_id >= boardgames.length){
            boardgame_div.style.display = "none";
            // alert("DONE");
        } else {
            boardgame_div.style.display = "";
            boardgame_img.setAttribute("src", boardgames[current_id].image);
            boardgame_name.innerHTML = boardgames[current_id].name;
            counter++;
        }
    }
    if(counter == 0){
        grid.style.display = "none";
        document.getElementById('no_games').style.display = "";
    } else {
        grid.style.display = "";
        document.getElementById('no_games').style.display = "none";
    }
}