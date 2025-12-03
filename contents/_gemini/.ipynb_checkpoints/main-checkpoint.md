

% #basic #direction change #intersection

$$ \overline{AE}^2 = \overline{EF} \cdot \overline{EG} $$ 
을 보여라. 

![Figure](figures/main_extract-figure0.svg)

다음 그림에서 두 색으로 표현된 두 삼각형의 비는 같을 것이다.
begin{figure}[H]
begin{subfigure}{0.49textwidth}

![Figure](figures/main_extract-figure1.svg)

$\frac{\overline{AE}}{\overline{EF}} = \frac{\overline{BE}}{\overline{ED}}$
end{subfigure}  %%%%%%%%%
begin{subfigure}{0.49textwidth}

![Figure](figures/main_extract-figure2.svg)

$\frac{\overline{BE}}{\overline{ED}} = \frac{\overline{EG}}{\overline{AE}}$
end{subfigure}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Caption
end{figure}

% #basic #direction change #연장선

%problem start
2021학년도 한과영 1-(6) 번, 16회 KMO 3번 

$\angle BEM = \angle DEM$이라고 할 때, 
$\frac{\overline{EP}}{\overline{BP}}$를 구하여라. 

![Figure](figures/main_extract-figure3.svg)

%problem end

한 변의 길이는 1로 가정한다.
begin{figure}[H]
begin{subfigure}{0.5textwidth}

![Figure](figures/main_extract-figure4.svg)

$\overline{BM}\perp\overline{EF}$ 

end{subfigure}
begin{subfigure}{0.5textwidth}

![Figure](figures/main_extract-figure5.svg)

$ \triangle BCM \sim \triangle MDE \Longrightarrow \overline{ED}= \frac 1 4$         

end{subfigure} %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

vspace{1cm}
불필요한 부분을 지우고 연장선을 하나 그리면 
$\overline{BP} : \overline{EP}$ 가 보인다.

begin{subfigure}{1textwidth}

![Figure](figures/main_extract-figure6.svg)

$\overline{BP} : \overline{EP} = \overline{BG} : \overline{AE}$     

end{subfigure}
end{figure}

이 문제를 처음 만났을 때의 풀이는 앞서의 것은 아니었다. 
부끄럽게도 이등변삼각형의 중선($BM$)이 밑변($EF$)과 수직임을 보지 못했었는데... 

이런 점이 기하가 어렵게 느껴지는 이유일터, 
추가되는 정보들이 많아지면 간단한 사실조차 알아보기 쉽지 않다. 
이번에도 한 변의 길이는 1로 가정한다.

begin{figure}[H]
begin{subfigure}{0.5textwidth}

![Figure](figures/main_extract-figure7.svg)

$\overline{BE}=\overline{BF}$ 

end{subfigure}
begin{subfigure}{0.5textwidth}

![Figure](figures/main_extract-figure8.svg)

직각삼각형 $(1+x)^2 = (1-x)^2 + 1$        

end{subfigure} %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
vspace{1cm}
피타고라스 정리에서 $x=\overline{ED}=\frac 14 $를 얻으면 다음 과정은 앞선 풀이와 같다.
begin{subfigure}{1textwidth}

![Figure](figures/main_extract-figure9.svg)

$\overline{BP} : \overline{EP} = \overline{BG} : \overline{AE}$     

end{subfigure}
end{figure}

앞서의 풀이보다 이 풀이가 더 긴 것은 아니지만, 
어떤 방법이 더 간결할 것인지에 대한 판단에 따른 것이 아니었으니 반성이 필요했다. 
웃기는 건 나중에 알게된 KMO 공식풀이는 이보다 훨씬 길고 복잡했다는 것이다. 

그림을 회전시키면 자신의 풀이도 알아보기 힘들다.  
다음 그림들 각각에 대해서 풀이를 만들어 보자.
begin{figure}[H]
begin{subfigure}{0.5textwidth}

![Figure](figures/main_extract-figure10.svg)

end{subfigure}
begin{subfigure}{0.5textwidth}

![Figure](figures/main_extract-figure11.svg)

end{subfigure} %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
vspace{1cm}

begin{subfigure}{0.5textwidth}

![Figure](figures/main_extract-figure12.svg)

end{subfigure}
begin{subfigure}{0.5textwidth}

![Figure](figures/main_extract-figure13.svg)

end{subfigure}
end{figure}

이런 원이 튀어 나왔다! $\angle EMB =  90^\circ$이라는 것, 즉 $\triangle EMB$가 직각삼각형임이 느껴지는가?
그런데 이 원은 어디쓰지?

%  category : 정사각형, 나선 닮음, 공원점
% #concyclic points, #공원점

38회(2024) KMO 중등부 1차 11번  
정사각형 $ABCD$에서 변 $AB$ 위의 점 $P$와 변 $AD$위의 점 $Q$는 
$\overline{AP} = \overline{AQ} = \frac{\overline{AB}}{5}$를 만족한다. 
점 $A$에서 선분 $PD$에 내린 수선의 발을 $H$라 하자. 삼각형 $APH$의 넓이가 20일 때, 
삼각형 $HCQ$의 넓이를 구하여라. 

% 정사각형 $ABCD$에서 변 $AB$ 위의 점 $P$와 변 $AD$위의 점 $Q$는 
% $\overline{AP} = \overline{AQ} = \frac{\overline{AB}}{5}$를 만족한다. 
% 점 $A$에서 선분 $PD$에 내린 수선의 발을 $H$라 하자. 삼각형 $APH$의 넓이가 20일 때, 
% 삼각형 $HCQ$의 넓이를 구하여라.  

![Figure](figures/main_extract-figure14.svg)

vfill

% 비율이 $\overline{AP}:\overline{AB}= 1:5$이면 그림을 보기 힘들다. 
% 위 그림은 $1:4$로 변경하여 그렸다.

begin{figure}[H]
begin{subfigure}{0.5textwidth}

![Figure](figures/main_extract-figure15.svg)

end{subfigure}
begin{subfigure}{0.5textwidth}

![Figure](figures/main_extract-figure16.svg)

end{subfigure}
vspace{1cm}
헉, 또 원이 튀어 나왔다. 이번에는 도움이 될까?

begin{subfigure}{0.5textwidth}

![Figure](figures/main_extract-figure17.svg)

end{subfigure}
begin{subfigure}{0.5textwidth}

![Figure](figures/main_extract-figure18.svg)

end{subfigure}
end{figure}

vfill

% #medium #right angles #concyclic points
$\overline{AB}=\overline{AC}$인 이등변삼각형 $ABC$에서 
$A$에서 선분 $BC$에 내린 수선의 발을 $D$라 하자. 
$D$에서 선분 $AC$에 내린 수선의 발을 $E$라 하고 선분 $DE$의 중점은 $M$이라 하자. 
이때 $\overline{AM} \perp \overline{EC}$임을 보여라. 

![Figure](figures/main_extract-figure19.svg)

![Figure](figures/main_extract-figure20.svg)

setcounter{prob}{0}

endnote{
% 34회(2020) KMO 중등부 1차 1번 
%답 : 10
%import{images}{38_20}
}
이 팔각형의 넓이를 구하여라.
vfill

endnote{
34회(2020) KMO 중등부 1차 1번 
답 : 10
%import{images}{38_20}
}
변 $BC$ 위의 점 $D$를 $\angle ADC = 120^\circ$가 되도록 잡고, 각 $C$의 이등분선과 
변 $AB$의 교점을 $E$라 하자. $\angle DEC$는 몇 도인가?
vfill

답 : 30

점 $D$는 선분 $AC$ 위에 있고 $\angle ABD=90^\circ$이다. 
점 $E$ 또한 선분 $AC$위에 있고 선분 $BD$는 $\angle CBE$의 이등분선이다. 
$\overline{BE}=5$일 때, $3\overline{CE}$의 값을 구하여라.
vfill 

답 : 80

$\angle A$의 이등분선 위에 $\overline{AD}=2$가 되는 점 $D$를 삼각형의 내부에 잡으면 
$\overline{CD} : \overline{BC} = 1:3$이 된다. 
$ADC$의 넓이를 $S$라 할 때, $5 S^2$를 구하여라. 
vfill

begin{sloppypar}
endnote{
%fbox{ 37회(2023) KMO 고등부 1차 6번 }
답 : 399
%import{images}{h23_6}
원주각과 중심각 관계를 생각하면 선분 $AB$와 선분 $DE$가 
지름이 빗변인직각삼각형의 나머지 두 변이 된다.
}
$\overline{AB}=1 \; , \; \angle BAC = \angle ACE = \angle CED = 30^\circ$ 일 때, 
$\overline{DE}^2$의 값을 구하여라.  
end{sloppypar}
vfill 

28회(2014) KMO 중등부 1차 4번 
답 : 280

변 $AB$위의 점 $M$을 중심으로 하고 두 변 $AC, BC$와 모두 접하는 원의 반지름이 12이다. 
변 $AB$의 $B$쪽으로의 연장선 위의 점 $N$을 중심으로 하고 점 $B$를 지나며 직선 $AC$와 
접하는 원이 직선 $AB$와 만나는 점을 $D(\not=B)$라 하자. 
$\overline{AM}=15$ 일 때, 선분 $BD$의 길이를 구하여라.
vfill 

28회(2014) KMO 중등부 1차 13번 

삼각형 $IBC$와 $IAC$의 외심을 각각 $U,V$라 하자. 점 $D$가 선분 $UV$ 위에 있고 
선분 $BV$와 변 $AC$가 점 $K$에서 만난다. $\overline{BD}=32 \; , \; \overline{KE}=18$일 때, 
삼각형 $ABC$의 내접원의 반지름을 구하여라. 
vfill

begin{sloppypar}

26회(2012) KMO 중등부 1차 19번 
답 : 45 

직선이 직선 $BC$와 점 $D$에서 만난다. 
$\overline{AB}=30, \overline{CA}=60, \overline{CD}=50 $ 일 때, 
선분 $BC$의 길이를 구하여라.
end{sloppypar} 
vfill

