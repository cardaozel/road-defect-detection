% Phase 4: Chapter 1 - Introduction - LaTeX Ready Version
% Copy the content below into your Overleaf Chapter 1 section

\chapter{Introduction\label{cha:chapter1}}

This thesis deals with the increasing need to have efficient and reliable road defect
monitoring in municipal maintenance systems. The state of road surfaces has a direct effect
on safety, transport efficiency, and infrastructure costs in the long run, which makes defect
detection a critical issue to the community agencies \cite{worldroad2021,roadmaintenance2022}. The main idea of the work is the use of on-device computer vision to
automatically detect surface-damage in real operation conditions. Traditional inspection
approaches are labour intensive, irregular and they do not scale well in large road networks
\cite{manualinspection2020}. The latest developments in deep learning and mobile acceleration have created potential on-site analysis on commodity devices \cite{edgeml2021,coreml2023,neuralengine2022}. However, in a modern system, the integration of the detection
models and the field reporting is still very limited and scattered \cite{smartcitysurvey2021}. This
thesis, in turn, focuses on end-to-end deployment of real-time detection and municipal
reporting on \gls{ios} devices, with the municipal context as the main user scenario instead
of the peripheral one, and the quality of detection evaluated through the applicability to
agencies with limited resources \cite{terven2023}.

The study is executed in a complete pipeline which includes model training and the
deployment of a mobile app. This thesis trains a compact object detector on the Road
Damage Dataset 2022 (\gls{rdd2022}) that provides standardized labels of six defect types and enables reproducible assessment \cite{rdd2022,rdd2020_2021,svrrd_2024}. \gls{yolov8s}
is selected as a compromise between accuracy and mobile computing limitations with
the goal of taking advantage of the latest developments in detection \cite{yolov8,terven2023}. The resulting model is then translated to \gls{coreml}
and incorporated into a \gls{swiftui} application to enable real-time camera inference and offline
processing on \gls{ios} devices \cite{coreml2023,swiftui2022}. The system has \gls{gps}-powered location tagging and reporting interface, which connects detections with contact information
of municipal authorities \cite{geomobility2021}. This end-to-end workflow of dataset preparation to
municipal reporting is shown in Figure~\ref{fig:pipeline}. The thesis is an assessment of technical
performance as well as practical usefulness with a focus on operational limits in the real
world. These considerations influence the aim of the research and the format of the successive chapters. The pipeline is designed to be reproducible such that the future researchers
can reproduce and compare the outcomes \cite{zaidi2021}.

\begin{figure}[t]
    \centering
    \includegraphics[width=0.90\linewidth]{figures/figure_pipeline.png}
    \caption{End-to-end pipeline from \gls{rdd2022} training to on-device reporting.}
    \label{fig:pipeline}
\end{figure}

\section{Motivation}

The damage of the roads is constantly increasing due to traffic overloads, seasonal changes
in weather, and the aging of materials, and late remediation usually increases the cost
of repair and safety threats \cite{pavementreview2021}. The municipal agencies have a large road
network that they are supposed to maintain and they have to focus on inspection and maintenance activities with a tight budget and restricted staff. Manual inspection is still the
most common in most areas due to its simplicity in organization; however, it is also subject
to inconsistency and cannot be scaled \cite{manualinspection2020}. Quality of inspection
is also usually different among the inspectors and under prevailing conditions which reduces reliability of decisions taken during maintenance. In densely populated cities, defects are bound to form quickly because of the large volumes of traffic and construction work,
and this means that they need to be monitored frequently. On the other hand, localities
with low-traffic and rural settings have a low frequency of inspection, which allows defects
to worsen without being detected. Such limitations drive the creation of automated and low-cost detection tools that can be used in large quantities without specialised equipment \cite{smartcitysurvey2021}. Late detection can also increase the risk of liability and upset
the expected maintenance plans. Automated monitoring provides a way to decrease the backlog and concentrate the resources on the most serious defects. With the introduction of mobile computing and on-device inference, a realistic avenue to field-deployable
inspection tools is available. Modern smartphones have specific neural acceleration chips
that can run deep-learning models in real-time speeds \cite{neuralengine2022}. This feature assists
on-device processing which maintains privacy, removes cloud latency and lowers the cost
of operation. In case of municipal use, the deployment of mobile can be viewed as a continuation of current work practices because the inspector can always have a smartphone
with him or her in the field. However, mobile deployment has severe limitations on model
size, inference latency and energy consumption that makes model selection and optimisation a critical consideration \cite{edgeml2021,mobiledets_2020}. Server grade GPUs,
which are designed into models, are often too large or too slow to be implemented on
the device, making direct adoption challenging. This means that the drive is not only
to attain acceptable accuracy but to realise operational feasibility on commodity devices.
Continuous inspection sessions also depend on battery life and thermal stability. All these
practical considerations make lightweight and efficient models a need and not an option \cite{pp_yoloe_2022}. In addition to the accuracy of detection, municipal maintenance needs
to be reported in a way that would enable the authorities to correlate the defects they
observe with those in charge. Numerous scholarly studies focus on the work of detection
but do not examine how the results of detection are communicated, stored, or escalated to
repair processes \cite{smartcitysurvey2021}. Even highly accurate detections without reporting
mechanisms do not become maintenance actions. A practical system should then assign
location, time, and context of defects to each detection, which would make this information
valuable in decision-making. Reporting capabilities can be integrated into the detection
process to relieve the administrative load and enhance responsiveness. This thesis has a
technical and operational motivation therefore: to provide an accurate detection model and
to incorporate it into a workflow that can maintain itself in the real world. Prioritisation,
auditing, and accountability across districts are also based on reporting, which increases
the utility of the results in strategic planning and budgeting. The ambiguity can also be
minimised by using standardised reporting forms whereby there is more than one agency
that has the responsibility of a road segment. Such an end-to-end perspective separates
real-world deployment and research prototypes that stop at detection.

\section{Research gap}

Existing road damage detection studies report strong accuracy but often stop at offline evaluation, leaving integration with field reporting and on-device deployment under-specified \cite{smartcitysurvey2021}. At the same time, many high-accuracy detectors rely on server-grade compute and are not validated under mobile constraints \cite{edgeml2021}. This creates a practical gap between benchmark performance and real municipal use, where privacy, latency, and operational simplicity are required. This thesis addresses the gap by combining a compact detector with a mobile reporting workflow designed for field use on commodity devices.

\section{Objective}

This thesis aims at the design and validation of an on-device road defect detection system
that assists in the practical municipal reporting. The system will have to identify six types
of defects in the \gls{rdd2022} dataset with the help of a small \gls{yolov8s} model that can be
inferred on a mobile device \cite{rdd2022,yolov8}. It needs to run in real time
on \gls{ios} devices on \gls{coreml} and maintain the detection accuracy after the conversion of
the model \cite{coreml2023}. This goal will also include building a \gls{swiftui} app that will be
capable of live camera inference, photo-library analysis, and detection history management
\cite{swiftui2022}. Location tagging is an essential feature since it will allow geo-referenced
reporting and tracking of the detected defects \cite{geomobility2021}. The system should have a
reporting interface that connects detections with authority contact information to ensure
that the time between detection and remedial action is reduced. Figure~\ref{fig:app-workflow} shows the
desired user process through capture to reporting. Lastly, the task involves assessing the
performance of detection, usability, and inference speed to show a real-world possibility
\cite{zaidi2021}. The purpose also implies that the mobile workflow should be simple
enough to avoid overcomplicated use by non-technical people in the field. An additional
objective is to ensure that the model outputs are predictable as well as interpretable in
different road conditions.

\begin{figure}[t]
    \centering
    \includegraphics[width=0.95\linewidth]{figures/figure_app_workflow.png}
    \caption{Mobile application workflow from capture to reporting.}
    \label{fig:app-workflow}
\end{figure}

\section{Research questions}

The research questions define measurable targets and link technical performance to practical deployment. They are summarized here and detailed further in Chapter~\ref{cha:chapter4}.

\textbf{RQ1:} What is the detection accuracy and performance of a \gls{yolov8s}-based model trained on \gls{rdd2022} for road defect detection \cite{rdd2022,yolov8}? \newline\newline
\textbf{RQ2:} Can the trained model be deployed on \gls{ios} devices using \gls{coreml} while maintaining real-time inference performance and acceptable accuracy after conversion \cite{coreml2023}? \newline\newline
\textbf{RQ3:} What are the usability characteristics and practical effectiveness of a mobile application that integrates detection with location-aware municipal reporting \cite{swiftui2022}?

\section{Contributions}

The main contributions of this thesis are:
\begin{enumerate}
    \item An end-to-end pipeline that connects \gls{rdd2022} training with on-device inference and municipal reporting on \gls{ios} \cite{rdd2022,coreml2023}.
    \item A compact \gls{yolov8s} model configuration optimized for mobile feasibility with reported accuracy and inference performance \cite{yolov8}.
    \item A \gls{swiftui} application that supports real-time inference, detection history, and location-aware reporting workflows \cite{swiftui2022,geomobility2021}.
    \item Reproducible documentation of training, deployment, and evaluation procedures to support future comparisons \cite{cardaozel2026}.
\end{enumerate}

\section{Problem Statement}

The existing road inspection systems are restricted by the use of manual labour, inconsistency, and lack of coverage thus slowing the process of defect correction and increasing the risk of road accidents \cite{manualinspection2020}. There are automated solutions but they often require specialised sensors, offline processing pipelines, or cloud infrastructure, which restrict flexibility of deployment and increase the cost of operation \cite{pavementreview2021,edgeml2021}. Numerous detection studies emphasise accuracy but do not include an end-to-end workflow that makes field reporting, location tracking, and actionable communication with responsible authorities possible \cite{smartcitysurvey2021}. The issue that has been discussed in this thesis is the lack of a lightweight, reliable and practical on-device system that can identify road defects in real-time and also support municipal reporting in the field conditions. The variability of the environment in terms of lighting, weather, and camera perspective worsens this issue and reduces the reliability of detection \cite{yu2024}. Figure~\ref{fig:road-defect-examples} illustrates some types of defects and visual variance in the \gls{rdd2022} dataset \cite{rdd2022}. The study is thus aimed at a mobile-friendly detection pipeline with inference, localisation and reporting all in one working tool \cite{yolox2021,pp_yoloe_2022}. This system has to run on-site without requiring consistent connectivity thus eliminating the need of many cloud-based solutions. It should also be able to come out with evidence that will not require a lot of manual reformatting in order to be presented to the decision makers.

\begin{figure}[t]
    \centering
    \includegraphics[width=0.85\linewidth]{figures/figure_defect_examples.png}
    \caption{Examples of the six RDD2022 defect classes and visual variability.}
    \label{fig:road-defect-examples}
\end{figure}

\section{Thesis Scope}

This thesis is restricted to on-device detection of six types of commonly occurring road
defects according to \gls{rdd2022}, such as longitudinal cracks, transverse cracks, alligator
cracks, potholes, white-line blur, and other defects \cite{rdd2022}. The thesis focuses on a single-stage detection system that can be applied to a mobile device, namely
\gls{yolov8s}, and does not explore larger versions that are resource-intensive on a server
\cite{yolov8,yolov7_2022,yolov9_2024}. The deployment targets include \gls{ios} devices using \gls{coreml}; Android is out of the scope of this
work \cite{coreml2023}. The thesis does not attempt to develop new detection architectures,
rather it evaluates the performance of an existing architecture when optimised to run on
mobile inference. Figure~\ref{fig:inference-architecture} gives a brief overview of the inference pipeline that is used in-device. The system is tested on the validation split of \gls{rdd2022}; there is no massive field
testing of municipal agencies in this study. It consists of a native \gls{swiftui} application that
can perform real-time inference, \gls{gps} tagging, and reporting, but not the integration with
external maintenance-management systems. These limits guarantee an intensive study of
viability and efficiency in a limited mobile setting. LiDAR or radar sensor fusion are not considered; only RGB imagery is used. It is also not discussed in the study how long-term fleet
management or automatic repair scheduling can be done.

\begin{figure}[t]
    \centering
    \includegraphics[width=0.85\linewidth]{figures/figure_model_architecture.png}
    \caption{On-device inference pipeline using YOLOv8s and CoreML runtime.}
    \label{fig:inference-architecture}
\end{figure}

\section{Purpose and goal}

This thesis is aimed at resolving the gap between academic and real-life municipal maintenance workflows and detection models. This is aimed at delivering a system that is
operationally viable and which can be deployed by the field workers without specialised
equipment or permanent connectivity. One of its key objectives is to reach a reasonable detection rate, at the same time maintaining the model size and latency within
the mobile constraints, making it possible to conduct inspection in the field in real time
\cite{edgeml2021,neuralengine2022}. The other objective is to incorporate the location-relevant reporting to minimize the administrative cost of recording defects and reporting to the authorities \cite{smartcitysurvey2021}. Figure~\ref{fig:app-workflow} highlights the process of examining the results of detection and reporting in the mobile application. The study will also result in reproducible training and evaluation processes that can be reused in subsequent datasets or deployment scenarios \cite{zaidi2021}. Combining detection and reporting, the system focuses on enhancing response times and documentation quality of municipal maintenance. Finally, the aim is to indicate that on-device road defect detection can be realistic, scalable, and implementable in real-life scenarios. Another reason is to make the workflow transparent, thus, building trust of the stakeholders in the provenance of detections. The thesis is also aimed at demonstrating that without cloud dependencies, it is possible to achieve meaningful reporting.

\section{Outline\label{sec:outline}}

This section outlines the structure of the thesis titled \textit{On-Device Road Damage Detection
for Municipal Reporting}. The thesis is divided into seven chapters, which are arranged
according to the research process background to conclusions. The different chapters add
certain elements of the system design, implementation, and evaluation. The following
outline gives a brief description of the content and role of each chapter. The titles of
the chapters are similar to the titles of the final sections in this thesis. The sequence is
deliberate in order to have conceptual underpinnings first followed by design decisions, and
then evaluation. This format helps the reader to relate technical choices with the real-world
limitations that drive the thesis. It also explains the location of evidence provided and the
way that the findings justify the ultimate assertions. The outline is not lengthy so that
one can quickly go through the document. It also illustrates the support of the research
questions and the final conclusions by each chapter.

\textbf{Chapter \ref{cha:chapter2} (Theoretical Background)} 
Presents the principles of object detection, machine learning on the mobile platform, and road defect taxonomy used in the proposed system. It outlines the main notions used throughout the thesis and summarizes important standards and technologies. The chapter describes how modern detection pipelines are designed and why one-stage models are preferred for real-time use. It also presents anchor-based and anchor-free paradigms to clarify later design decisions. On-device inference constraints are addressed to contextualize mobile deployment requirements. High-level diagrams explain detection flow, the on-device stack, and data structure. Evaluation measures and dataset composition are summarized to define the measurement framework used later. The chapter provides the conceptual framework for interpreting methodological decisions and deployment limitations in later chapters. It also serves as a source of terminology used in the methods and results sections.

\textbf{Chapter \ref{cha:chapter3} (Related Work)} reviews the literature on road damage detection, dataset construction, and on-device inference. It compares traditional computer-vision approaches with deep-learning techniques and outlines the drawbacks of existing mobile systems. The literature is classified by detection architecture, deployment strategy, and dataset focus, which reveals current design patterns. A taxonomy figure summarizes these categories for quick comparison. A summary table highlights the datasets, performance variables, and deployment settings used in recent studies. The survey focuses on publications after 2020 to align with the thesis reference policy. By comparing approaches, the chapter clarifies gaps in end-to-end municipal reporting workflows. These results motivate the originality of the thesis and place the study within contemporary scholarship. The chapter also identifies the methods most appropriate for mobile deployment.

\textbf{Chapter \ref{cha:chapter4} (Research Question)} 
systematises the research problem and describes the guiding research questions. It outlines goals related to detection accuracy, real-time operation, and usability in municipal field settings. The research questions are stated to cover model performance, deployment feasibility, and reporting usability. The chapter defines the research area and identifies factors that are deliberately excluded. It links the questions to quantifiable results discussed in later chapters. This framing ensures that evaluation measures align with the objectives stated at the beginning of the thesis. The chapter therefore acts as a contractual connection between the problem definition and the results presented later. It provides clear requirements for judging whether the proposed system serves its purpose. The section also provides a direct line from research questions to the respective experiments and results.

\textbf{Chapter \ref{cha:chapter5} (Methods)} 
details the dataset, preprocessing steps, model architecture, training strategy, and software environment. It describes the CoreML conversion process and the integration of the model into a SwiftUI application. The chapter explains how augmentation and validation are handled so that training is stable and reproducible. It also documents the software stack and configuration files used to run experiments. Tables and figures are included to summarize hyperparameters, software components, and evaluation metrics. The chapter includes guidance on how the model and application are built from the repository materials. This chapter provides the technical steps needed to reproduce the results and to understand the deployment pipeline. The methods section therefore connects research goals to implementable procedures. It also clarifies how results can be validated by other researchers.

\textbf{Chapter \ref{cha:chapter6} (Experiments and Results)} outlines the results of training, validation metrics, and mobile inference performance. It describes experimental studies that assess generalisation, compares results with baseline procedures, and explains the trade-offs observed. The chapter contains figures for training curves, precision--recall behavior, confusion matrices, and detection examples. It also outlines the training environment and summarizes checkpoints and evaluation tables to improve clarity. End-user performance metrics from the \gls{ios} application are reported to connect empirical results with user-facing performance. The discussion clarifies the conditions where the model performs well and outlines limitations that reduce accuracy. Error analysis is included to explain the most frequent failure modes observed during testing. Overall, this chapter provides the empirical basis for the conclusions in Chapter 7 and links observations to the research questions posed earlier.

\textbf{Chapter \ref{cha:chapter7} (Conclusion)} presents the work of the proposed system in a concise manner, its limitations, and outlines the future research directions. It is a critical analysis of the progress of the system in terms of developing municipal reporting and enabling deployment on a device, therefore, it bridges the gap between developing the theory and real implementation. The methodological steps taken during the thesis are revisited and related systematically to the major research questions. It determines the most salient restrictions that appeared during training and deployment and offers a clear description of the challenges discussed. Dissemination is expressed in terms of the user communities that benefit from the system, and how the technology can be incorporated into current municipal workflows. The analysis evaluates consequences for stakeholder participation and operational scalability. The future view provides specific improvements to advance accuracy, generalization, and platform coverage. The chapter concludes by translating the empirical findings into actionable guidance for municipal stakeholders and by outlining measures to extend the system to wider real-world settings. It also advises that future studies should build on the reproducible pipeline presented in this study.
