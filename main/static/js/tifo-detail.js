const dateInput = document.getElementById('id_date');
if (dateInput) {
  const picker = MCDatepicker.create({
    el: '#id_date',
    dateFormat: 'yyyy-mm-dd',
    closeOnBlur: true,
    selectedDate: new Date()
  });

  dateInput.addEventListener("click", () => {
    picker.open();
  });
}
