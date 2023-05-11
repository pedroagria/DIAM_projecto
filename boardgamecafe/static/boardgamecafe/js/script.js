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

// GLOBAL VARIABLE TO USE HAS PAGE INDEX
var page_index = 1;
var active_filter = true;

// FOR GAME FILTERING IN LIST OF GAMES
function filterBoardGames(new_page_index){
    var parsed_boardgames = JSON.parse(all_boardgames);
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
       if(active_filter){
           if(!parsed_boardgames[i].log_is_active){
               continue;
           }
       }
       filteredBoardGames.push(parsed_boardgames[i]);
    }
    constructListPage(filteredBoardGames, new_page_index);
}

// FOR SHOWING CORRECT GAMES IN LIST
function constructListPage(boardgames, new_page_index){
    var grid = document.getElementById('boardgames_grid');
    var divs = grid.getElementsByTagName('a');
    var counter = 0;
    var number_of_games = boardgames.length;
    for(var i = 0; i < 9; i++){
        var boardgame_div = divs[i];
        var boardgame_img = boardgame_div.getElementsByTagName('img')[0];
        var boardgame_name = boardgame_div.getElementsByTagName('h3')[0];
        var current_id = (new_page_index - 1) * 9 + i;
        if(current_id >= number_of_games){
            boardgame_div.style.display = 'none';
        } else {
            boardgame_div.style.display = '';
            boardgame_img.setAttribute('src', boardgames[current_id].image);
            // boardgame_div.setAttribute('href', "{% url 'boardgamecafe:game' '" + boardgames[current_id].id + "' %}");
            boardgame_div.setAttribute('href', "game/" + boardgames[current_id].id);
            boardgame_name.innerHTML = boardgames[current_id].name;
            counter++;
        }
    }
    if(counter == 0){
        grid.style.display = 'none';
        document.getElementById('no_games').style.display = '';
    } else {
        grid.style.display = '';
        document.getElementById('no_games').style.display = 'none';
        page_index = new_page_index;
        var max_pages = number_of_games / 9.00;
        if(max_pages == 1){
            $('#page_index_text').text("");
        } else{
            $('#page_index_text').text(page_index);
        }
        if(page_index == 1){
            $('#previous_page_button').css('visibility', 'hidden');
        } else {
            $('#previous_page_button').css('visibility', 'visible');
        }
        if(page_index < max_pages){
            $('#next_page_button').css('visibility', 'visible');
        } else {
            $('#next_page_button').css('visibility', 'hidden');
        }
    }
}

// TO ALTER ACTIVE FILTER IN LIST OF GAMES
function changeActiveFilter(){
    if($("#log_is_active_checkbox").is(":checked")){
        active_filter = false;
    } else{
        active_filter = true;
    }
    filterBoardGames(1);
}