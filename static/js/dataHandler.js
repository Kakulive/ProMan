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
        let response = await apiPost(`/create-new-card/${boardId}/${cardTitle}/${columnId}`);
        return response
        // creates new card, saves it and calls the callback function with its data
    },
    getLatestCardId: async function () {
        let response = await apiGet(`/get-latest-card-id`);
        return response
    },
    getFirstColumnFromBoard: async function (boardId) {
        let response = await apiGet(`/get-first-column-from-board/${boardId}`);
        return response
    },
    deleteCard: async function (cardID) {
        let response = await apiGet(`/delete-card/${cardID}`)
        return response
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

async function apiPost(url) {
    let response = await fetch(url, {
        method: 'POST',
    })
}

async function apiDelete(url) {
}

async function apiPut(url) {
}
