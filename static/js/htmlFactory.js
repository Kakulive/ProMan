export const htmlTemplates = {
    board: 1,
    card: 2,
    column: 3
}

export function htmlFactory(template) {
    switch (template) {
        case htmlTemplates.board:
            return boardBuilder
        case htmlTemplates.card:
            return cardBuilder
        case htmlTemplates.column:
            return columnBuilder
        default:
            console.error("Undefined template: " + template)
            return () => { return "" }
    }
}

function boardBuilder(board) {
    return `<div class="board-container">
                <section class="board${board.id}" data-board-id="${board.id}" id="board${board.id}">
                    <div class="board-header">
                        <span class="board-title">${board.title}</span>
                        <button class="board-add" data-board-id="${board.id}">Add Card</button>
                        <button class="column-add" data-board-id="${board.id}">Add Column</button>
                        <button class="board-toggle" data-board-id="${board.id}"><i class="fas fa-chevron-down"></i></button>
                    </div>
                    <div class="board-columns" data-board-id="${board.id}"></div>
                </section>
             </div> `
}

function cardBuilder(card) {
    return `<div class="card" data-card-id="${card.id}" id="card${card.id}" draggable="true">
                <div class="card-remove" id="removeCard${card.id}"><i class="fas fa-trash-alt"></i></div>
                <div class="card-title" id="cardTitle${card.id}">${card.title}</div>
            </div>`;
}

function columnBuilder(boardId, column) {
    return `<div class="board-column" id="column${column.id}">
                    <div class="board-column-title">${column.status}</div>
                    <div class="board${boardId}-column-content" data-column-id="${column.id}"></div>
            </div>`
}
