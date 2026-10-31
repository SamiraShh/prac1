# prac1
```mermaid
flowchart TD
 Start([Вход: Qж, W, Pпл, Pзаб]) --> CalcDP[Депрессия: dP = Pпл - Pзаб]
 CalcDP --> CheckDP{dP > 0?}
 CheckDP -- Нет --> SetJZero[J = 0.0]
 CheckDP -- Да --> CalcJ[Продуктивность: J = Qж / dP]
 SetJZero --> Diag1{dP < 0?}
 CalcJ --> Diag1
 Diag1 -- Да --> CodeBlow[Код: BLOWOUT]
 Diag1 -- Нет --> Diag2{dP <= 0.5?}
 Diag2 -- Да --> CodeIdle[Код: IDLE]
 Diag2 -- Нет --> Diag3{W >= 85%?}
 Diag3 -- Да --> CodeWat[Код: WATERED]
 Diag3 -- Нет --> Diag4{J < J_norm?}
 Diag4 -- Да --> CodeClog[Код: CLOGGED]
 Diag4 -- Нет --> CodeNorm[Код: NORMAL]
 CodeBlow --> End([Вывод кода и директивы диспетчеру])
 CodeIdle --> End
 CodeWat --> End
 CodeClog --> End
 CodeNorm --> End
```
