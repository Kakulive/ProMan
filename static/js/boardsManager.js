import { dataHandler } from "./dataHandler.js";
import { htmlFactory, htmlTemplates } from "./htmlFactory.js";
import { domManager } from "./domManager.js";
import { cardsManager } from "./cardsManager.js";
import { columnsManager } from "./columnsManager.js";

export let boardsManager = {
    loadBoards: async function () {
        const boards = await dataHandler.getBoards();
        for (let board of boards) {
            const boardBuilder = htmlFactory(htmlTemplates.board);
            const content = boardBuilder(board);
            domManager.addChild("#root", content);
            domManager.addEventListener(`.board-toggle[data-board-id="${board.id}"]`,
                "click", showHideButtonHandler);
            domManager.addEventListener(`.board-add[data-board-id="${board.id}"]`,
                "click", createCard);
        }
    },
}

async function showHideButtonHandler(clickEvent) {
    const boardId = clickEvent.currentTarget.dataset.boardId;
    await columnsManager.loadColumns(boardId);
    await cardsManager.loadCards(boardId);
}


async function createCard(clickEvent) {
    const boardId = clickEvent.target.dataset.boardId;
    let cardId = await dataHandler.getLatestCardId();
    cardId ++ ;
    let columnId = await dataHandler.getFirstColumnFromBoard(boardId);
    const tempCard = {
        title: "title",
        id: cardId,
        column_id: columnId
    };
    const cardBuilder = htmlFactory(htmlTemplates.card);
    const content = cardBuilder(tempCard);
    domManager.addChild(`.board${boardId}-column-content[data-column-id="${tempCard.column_id}"]`,
                content)
    // domManager.addEventListener(`.card[data-card-id="${tempCard.id}"]`,
    //             "click", cardsManager.deleteButtonHandler)

    let userInput = document.createElement("input");
    userInput.setAttribute('id',tempCard.id)
    userInput.setAttribute('type', 'text');
    const cardIdString = "card" + tempCard.id.toString();
    const newCard = document.getElementById(cardIdString);
    newCard.removeChild(newCard.childNodes[3]); //removes the temporary title
    newCard.appendChild(userInput);

    userInput.addEventListener("keydown", function(event){
        if (event.keyCode === 13) {
            event.preventDefault();
            const titleDivToBeAdded = document.createElement("div")
            titleDivToBeAdded.setAttribute("class", "card-title")
            const titleText = userInput.value;
            titleDivToBeAdded.innerHTML += titleText;
            newCard.appendChild(titleDivToBeAdded)
            newCard.removeChild(newCard.childNodes[4]) //removes the input form
            dataHandler.createNewCard(titleText, boardId, tempCard.column_id)
        }
    })
}
