% Phase 4: Chapter 4 - Research Question - LaTeX Ready Version
% Copy the content below into your Overleaf Chapter 4 section

\chapter{Research Question\label{cha:chapter4}}

This chapter outlines the research questions that guide the thesis and streamline the real problem within the means of precise answers. Road-damage detection requires a detector to have high accuracy under heterogeneous visual conditions and to be lightweight enough for use on the road \cite{edgeml2021,yu2024}. In this connection, the research hypothesis consists of proposing an end-to-end system implementation with training, conversion, and on-device inference instead of using offline model evaluation only \cite{coreml2023,swiftui2022}. Such a wider scope is what makes it urgent to formalise questions related to detection performance, feasibility in real time, and usability in the field \cite{zaidi2021}. The chosen dataset and deployment stack provide a realistic testbed for these questions: \gls{rdd2022} provides standardised defect classes, and \gls{coreml} supports on-device inference \cite{rdd2022,coreml2023}. Recent sources point to the fact that deployment requirements and reporting procedures are often poorly defined, thus enabling clear research question settings that have an operational basis \cite{smartcitysurvey2021,edgeml2021}. Therefore, this chapter presents the research problem in a clear manner and suggests research questions that can be answered with quantifiable experiments and system verification. These questions develop the standards that will be used in the following chapters to identify the extent to which the proposed solution attains its targets. They also ensure that measurement metrics align with the operational needs of the system. The derived framework provides the thesis with concrete contributions as opposed to having single benchmark improvements only.

\section{Problem statement}

In municipal road inspection, manual processes are slow, disjointed, and hard to scale on large networks, which slows down maintenance and exposes people to more safety risks \cite{smartcitysurvey2021}. Despite the availability of automated detection models, most of them involve cloud infrastructure or hardware resources that field teams do not have, which limits their applicability in practice \cite{edgeml2021}. The imagery of road damages creates additional difficulties since defects are very small, elongated, and affected by changes in lighting and viewpoint \cite{yu2024}. To be practical, a detector should be able to run in real time on commodity mobile devices and have reasonable accuracy across various classes of defects \cite{rdd2022,yolov8}. Additionally, the outcomes of detection have to be combined with location-aware reporting to facilitate municipal decision-making, rather than generate bounding boxes only \cite{coreml2023}. The ability to work offline and privacy concerns are also considered when making deployment decisions, as field work is usually not well connected. Reporting should also be easy enough to use when there is a time limit but should be auditable in case it needs to be reviewed at some point. These limitations outline a gap between academic detection standards and implementation requirements. The gap discussed in this thesis is the lack of a lightweight, robust, and full-fledged on-device system that is able to recognise road damage and aid in reporting under field conditions. To address this gap and make evaluation concrete, the following research questions are formulated.

\section{Research questions}

\textbf{RQ1:} What is the detection accuracy and performance of a \gls{yolov8s}-based model when trained on the \gls{rdd2022} dataset for road defect detection \cite{rdd2022,yolov8}? This question focuses on \gls{map}, precision, and recall to measure whether a compact model can achieve competitive accuracy under dataset variability \cite{rdd2022}.\newline\newline
\textbf{RQ2:} Can the trained model be deployed on \gls{ios} devices using \gls{coreml} while maintaining real-time inference performance and acceptable accuracy after conversion \cite{coreml2023}? This question addresses runtime feasibility, latency constraints, and deployment stability on mobile hardware \cite{edgeml2021,coreml2023}.\newline\newline
\textbf{RQ3:} What are the usability characteristics and practical effectiveness of a mobile application that integrates detection with location-aware municipal reporting \cite{swiftui2022}? This question evaluates whether the workflow is actionable for field use, including detection history, \gls{gps} tagging, and reporting interfaces. Together, these questions align the technical goals of detection accuracy with the operational goals of on-device feasibility and reporting usability. The answers provide the evaluation framework for the methods and experiments presented in later chapters.


\section{Traceability matrix}

Table~\ref{tab:rq-traceability} maps each research question to the methods, metrics, and results sections where it is addressed. This provides a clear link from RQ to experimental evidence.

\begin{table}[t]
    \centering
    \caption{Traceability matrix from research questions to methods and results.}
    \label{tab:rq-traceability}
    \begin{tabular}{p{1.4cm} p{4.6cm} p{4.2cm} p{3.2cm}}
        \hline
        RQ & Methods (Chapter~\ref{cha:chapter5}) & Metrics & Results (Chapter~\ref{cha:chapter6}) \\
        \hline
        RQ1 & Dataset, training, model architecture & \gls{map}, precision, recall & Training metrics, validation summary \\
        RQ2 & \gls{coreml} conversion, \gls{ios} inference & Latency, model size & Mobile feasibility and inference results \\
        RQ3 & App workflow, reporting features & Usability evidence & Qualitative app results and reporting workflow \\
        \hline
    \end{tabular}
\end{table}
