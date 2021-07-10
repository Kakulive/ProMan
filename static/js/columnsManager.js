import { dataHandler } from "./dataHandler.js";
import { htmlFactory, htmlTemplates } from "./htmlFactory.js";
import { domManager } from "./domManager.js";

export let columnsManager = {
    loadColumns: async function (boardId) {
        const columns = await dataHandler.getColumnsByBoardId(boardId);
        for (let column of columns) {
            const columnBuilder = htmlFactory(htmlTemplates.column);
            const content = columnBuilder(boardId, column)
            domManager.addChild(`.board-columns[data-board-id="${boardId}"]`, content)
        }
    }
}
