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
                "click", showHideButtonHandler)
        }
    },
}

async function showHideButtonHandler(clickEvent) {
    const boardId = clickEvent.currentTarget.dataset.boardId;
    await columnsManager.loadColumns(boardId);
    cardsManager.loadCards(boardId);
}
