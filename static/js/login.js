  const bg = document.querySelector('.slider-bg');
  const radios = document.querySelectorAll('input[name="role"]');
  const labels = document.querySelectorAll('.role-label');

  function updateSlider() {
    const selected = Array.from(radios).findIndex(r => r.checked);
    bg.style.transform = translateX(${selected * 100}%);
    labels.forEach((lbl, i) => {
      lbl.style.color = i === selected ? '#fff' : '#555';
    });
  }

  radios.forEach(r => r.addEventListener('change', updateSlider));
  updateSlider();