export let dataHandler = {
    getBoards: async function () {
        let response = await apiGet('/get-boards');
        return response
    },
    getBoard: async function(boardId) {
        // the board is retrieved and then the callback function is called with the board
    },
    getStatuses: async function () {
        // the statuses are retrieved and then the callback function is called with the statuses
    },
    getStatus: async function (statusId) {
        // the status is retrieved and then the callback function is called with the status
    },
    getCardsByBoardId: async function (boardId) {
        let response = await apiGet(`/get-cards/${boardId}`);
        return response
    },
    getColumnsByBoardId: async function (boardId) {
        let response = await apiGet(`/get-columns/${boardId}`);
        return response
    },
    getCard: async function (cardId) {
        // the card is retrieved and then the callback function is called with the card
    },
    createNewBoard: async function (boardTitle) {
        // creates new board, saves it and calls the callback function with its data
    },
    createNewCard: async function (cardTitle, boardId, columnId) {
        let body_content = {
            "card_title": cardTitle,
            "board_id": boardId,
            "column_id": columnId
        };
        let response = await apiPost(`/create-new-card`, body_content);
        // creates new card, saves it and calls the callback function with its data
    },
    createNewColumn: async function (boardId, newColumnName, columnId) {
        let body_content = {
            "column_name": newColumnName,
            "board_id": boardId,
            "column_id": columnId
        };
        let response = await apiPost(`/create-new-column`, body_content);
    },
    getLatestCardId: async function () {
        let response = await apiGet(`/get-latest-card-id`);
        return response
    },
    getLatestColumnId: async function () {
        let response = await apiGet(`/get-latest-column-id`);
        return response
    },
    getFirstColumnFromBoard: async function (boardId) {
        let response = await apiGet(`/get-first-column-from-board/${boardId}`);
        return response
    },
    deleteCard: async function (cardId) {
        let response = await apiDelete(`/delete-card/${cardId}`)
    },
    updateCardTitle: async function (cardID, newTitleText) {
        let body_content = {
            "card_id": cardID,
            "new_title_text": newTitleText,
        };
        let response = await apiPut(`/update-card-title`, body_content)
    },
    updateCardOrder: async function (cardOrderNumber, cardId, columnId) {
        let body_content = {
            "card_order": cardOrderNumber,
            "card_id": cardId,
            "column_id": columnId,
        };
        let response = await apiPut(`/update-card-after-moving`, body_content)
    }
};

async function apiGet(url) {
    let response = await fetch(url, {
        method: 'GET',
    })
    if (response.status === 200) {
        let data = response.json()
        return data
    }
}

async function apiPost(url, body_content) {
    let response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body_content),
    })
}

async function apiDelete(url) {
    let response = await fetch(url, {
        method: 'DELETE',
    })
}

async function apiPut(url, body_content) {
    let response = await fetch(url, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body_content),
    })
}
