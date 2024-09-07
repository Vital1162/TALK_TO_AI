var pieceThemePath = "{% static 'chessboardjs-1.0.0/img/chesspieces/wikipedia/' %}";

config = {
    draggable: true,
    dropOffBoard: 'trash',
    position: 'start',
    pieceTheme: pieceThemePath + '{piece}.png'

}
var board = Chessboard('myBoard', config);