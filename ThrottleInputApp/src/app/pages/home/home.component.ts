import { Component, OnInit } from '@angular/core';

@Component({
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  value: number = 0;
  interval: NodeJS.Timeout;
  isActive: boolean;

  constructor() { }

  ngOnInit(): void {
  }

  pressButton(isActive: boolean): void {
    this.isActive = isActive
    clearInterval(this.interval);
    if (!this.value && !isActive) return; // Avoid negative values

    this.interval = setInterval(() => {
			this.value += isActive ? 1 : -1;
      if (this.value >= 100 || this.value <= 0) clearInterval(this.interval);
		}, 100);
  }

}
