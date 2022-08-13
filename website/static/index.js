function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ advertId: advertId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
