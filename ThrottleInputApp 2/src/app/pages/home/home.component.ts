import { Component, OnInit } from '@angular/core';
import { Data } from 'src/app/models/data';
import { QuixService } from 'src/app/services/quix.service';

@Component({
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  value: number = 0;
  interval: NodeJS.Timeout;
  isActive: boolean;

  constructor(private quixService: QuixService) { }

  ngOnInit(): void {
  }

  pressButton(isActive: boolean): void {
    this.isActive = isActive
    clearInterval(this.interval);
    if (!this.value && !isActive) return; // Avoid negative values

    this.interval = setInterval(() => {
			this.value += isActive ? 1 : -1;
      this.sendData(this.value);
      if (this.value >= 100 || this.value <= 0) clearInterval(this.interval);
		}, 10);
  }

  sendData(value: number): void {
    const payload: Data = {
      timestamps: [new Date().getTime() * 1000000],
      numericValues: {
        "speed": [value],
      }
    };
    const topicId = this.quixService.workspaceId + '-' + this.quixService.topicName;
    this.quixService.sendParameterData(topicId, 'test-bench', payload);
  }

}
