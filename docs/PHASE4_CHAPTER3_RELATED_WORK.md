% Phase 4: Chapter 3 - Related Work - LaTeX Ready Version
% Copy the content below into your Overleaf Chapter 3 section

\chapter{Related Work\label{cha:chapter3}}

This chapter reviews literature related to real-time object detection, mobile deployment, and road damage detection, which together form the technical basis of the thesis. The review is organized by subcomponents that align with the system pipeline: detection architectures, edge deployment techniques, and road damage datasets and task-specific methods. Each section groups papers by similarity in approach to highlight shared design choices and trade-offs. The primary goal is to identify techniques that enable accurate detection under resource constraints while remaining practical for municipal field use \cite{edgeml2021}. Recent work emphasizes end-to-end detection pipelines and hardware-aware design, which mirrors the thesis focus on on-device inference \cite{terven2023}. The literature also shows increasing attention to dataset quality and evaluation consistency across regions and capture conditions \cite{yu2024}. Figure~\ref{fig:ch3-taxonomy} provides a compact taxonomy of the related work categories used in this chapter. The summary of key works is consolidated in Table~\ref{tab:related-work-summary} for quick reference and comparison. Figure~\ref{fig:ch3-focus-counts} summarizes how the cited works distribute across focus areas, Figure~\ref{fig:ch3-year-counts} shows the publication year distribution for the summary set, and Figure~\ref{fig:ch3-focus-year} visualizes how focus areas evolve across recent years. Together, these summaries help ensure the review emphasizes recent, deployment-relevant research.

\begin{figure}[t]
    \centering
    \includegraphics[width=0.95\linewidth]{figures/figure_ch3_taxonomy.png}
    \caption{Taxonomy of related work grouped by detector family, deployment focus, and dataset or task emphasis.}
    \label{fig:ch3-taxonomy}
\end{figure}

\begin{table}[t]
    \centering
    \caption{Summary of key related work used in this thesis.}
    \label{tab:related-work-summary}
    \begin{tabular}{p{3.4cm} p{1.2cm} p{3.2cm} p{5.2cm}}
        \hline
        Reference & Year & Focus & Key Idea \\
        \hline
        \cite{yolov9_2024} & 2024 & Detection architecture & PGI and GELAN for efficient real-time detection. \\
        \cite{yolov10_2024} & 2024 & End-to-end detection & NMS-free YOLO with holistic efficiency design. \\
        \cite{rtdetr_2023} & 2023 & Transformer detection & Real-time DETR with hybrid encoder and fast decoding. \\
        \cite{yolo_world_2024} & 2024 & Open-vocabulary & Vision-language path aggregation for flexible detection. \\
        \cite{mobiledets_2020} & 2020 & Mobile detection & Architecture search tailored to mobile accelerators. \\
        \cite{pp_yoloe_2022} & 2022 & Industrial detector & Anchor-free design with deployment-friendly speed. \\
        \cite{rdd2022} & 2022 & Dataset & Multi-national road damage benchmark with six classes. \\
        \cite{rdd2020_2021} & 2021 & Dataset & Smartphone-based road damage annotations for benchmarking. \\
        \cite{svrrd_2024} & 2024 & Dataset & Street-view dataset for road damage detection. \\
        \cite{pham2022_yolov7} & 2022 & Road damage & YOLOv7 with coordinate attention for CRDDC2022. \\
        \hline
    \end{tabular}
\end{table}

\begin{figure}[t]
    \centering
    \includegraphics[width=0.75\linewidth]{figures/figure_ch3_focus_counts.png}
    \caption{Distribution of related work by primary focus area (summary counts).}
    \label{fig:ch3-focus-counts}
\end{figure}

\begin{figure}[t]
    \centering
    \includegraphics[width=0.75\linewidth]{figures/figure_ch3_year_counts.png}
    \caption{Publication year distribution for the summarized related work.}
    \label{fig:ch3-year-counts}
\end{figure}

\begin{figure}[t]
    \centering
    \includegraphics[width=0.9\linewidth]{figures/figure_ch3_focus_year.png}
    \caption{Related work focus by publication year (summary table).}
    \label{fig:ch3-focus-year}
\end{figure}

\section{Real-Time Detection Architectures}

Recent improvements with respect to real-time object detection focus on the \gls{yolo} family, where emphasis is on computational efficiency while maintaining object detection rates. YOLOv9, for example, has designed a novel concept to enhance gradient flow and lightweight performance through programmable gradient information and the GELAN architecture which is especially relevant for device constraints \cite{yolov9_2024}. By contrast, YOLOv10 removes the former requirement of non-maximum suppression (\gls{nms}) using a consistent dual assignment approach and refinement of model pieces for lessening the latency without the need to reduce accuracy \cite{yolov10_2024}. YOLOv8 continues to be popular as a base, thanks to its good speed-accuracy trade-off, and is a good baseline for targeting in mobile application settings \cite{yolov8}. A systematic review of the architectures of the \gls{yolo} family highlights the methods that have improved real-time performance, and thus the choice of a small version of \gls{yolo} for the current thesis \cite{terven2023}. Open vocabulary extensions like YOLO-vWorld confirm that the combination of vision and language forces can make detectors more flexible in their scope and yet they are less adjusted to strict mobile requirements \cite{yolo_world_2024}. Optimised YOLOv5s variants in pavement inspection. In the context of pavement inspection, some useful tricks may impact the system's accuracy while ensuring a small size \cite{yolov5s_2022}. 

 Transformer based detectors offer a good alternative for \gls{yolo}-styled pipelines since they reframe the detection problem from segmentation to object detection as a set prediction problem. RT-DETR presents \gls{detr}-like models that can achieve the performance similar to that of \gls{yolo} in real time by using a mixture of encoder and efficient decoder and achieve to challenge the dominance of one-stage convolutional neural network detectors \cite{rtdetr_2023}. Grounding DINO uses supervised language for open-set detection to support language grounding; open-set detection can replace fixed categories in object detection and thus extend the concept scope \cite{groundingdino_2023}. Such approaches prove that transformers can reduce or remove the need of post-processing techniques such as \gls{nms}, which can optimize deployment pipelines \cite{detr2020}. However, transformer detectors, in general, require significant computational and may be less desirable in an inflexible mobile latency requirement. For the detection of road damage, which is usually small and subtle, using dense convolution predictions has been suggested by the literature, which are competitive for fine-grained localisation. \gls{yolo}v7 and RTMDet offer good real time baselines which provides an example of this dense prediction efficiency in practice \cite{yolov7_2022,rtmdet_2022}. The juxtaposition of transformer and \gls{cnn}-based approaches puts the design trade-offs behind the choice of \gls{yolov8s} for this thesis in context. These results show that transformer efficiency continues to improve, but the process still requires the profiling of mobile targets with care \cite{rtdetr_2023}.

\section{Edge Deployment and Mobile Optimization}

Mobile and edge deployment research emphasizes resource-aware architecture design, compression, and inference optimization. MobileDets uses neural architecture search to optimize detection models for mobile accelerators, demonstrating that regular convolutions can be beneficial when placed strategically \cite{mobiledets_2020}. EfficientDet introduced compound scaling and \gls{bifpn} to produce a family of detectors with a strong speed--accuracy trade-off suitable for constrained devices \cite{efficientdet2020}. YOLOX and PP-YOLOE further improved real-time efficiency with anchor-free design, decoupled heads, and deployment-friendly optimizations \cite{yolox2021,pp_yoloe_2022}. RTMDet offers an empirical design study that shows how backbone--neck balance and soft label assignment can improve real-time accuracy at high \gls{fps} \cite{rtmdet_2022}. YOLOv7 continues this line of work by emphasizing trainable bag-of-freebies to improve accuracy without increasing inference cost \cite{yolov7_2022}. Architecture search and lightweight heads remain common strategies for edge detectors that must balance speed and accuracy \cite{mobiledets_2020,pp_yoloe_2022}. These methods illustrate the evolution toward detectors that can run effectively on edge hardware without compromising detection quality \cite{edgeml2021}. Additional deployment and efficiency-focused detection studies include \cite{edgeml2021,zaidi2021,mobiledets_2020}. This thesis takes \gls{yolov8s}, since this is an example of a contemporary trade-off point in accordance with this trajectory.

The practical limitations on on-device inference are constrained by the frameworks on which they're deployed and their hardware support. \gls{coreml} provides an optimised runtime for \gls{ios} that supports the transfer, quantisation and hardware acceleration of the model or models on the Apple Neural Engine \cite{coreml2023,neuralengine2022}. Surveys on on-device machine learning highlight the need for trade-offs among model size, power requirement in terms of memory footprint and power \cite{edgeml2021}, especially in a continuous camera inference scenario. YOLOv8 is often deployed in mobile settings due to its efficient model development and exportation functionality, hence making the model suitable for \gls{coreml} conversion processing \cite{yolov8}. Recent studies have shown that careful preprocessing and steady and consistent input size are key to achieving steady latency on mobile devices. Quantisation and operator fusion are usually vital for attaining stable frames per second on cellular accelerators \cite{edgeml2021}. These are the constraints that are used to aid in the choice of the model variant and the training configuration of this model, both of which are addressed explicitly in the methodology chapter. The success of mobile deployment is related to both system integration and model accuracy, the literature says. As a result, this thesis focuses more on end-to-end deployment than on performance of isolated model level.

\section{Road Damage Datasets and Task-Specific Methods}

Road-damage detection research is greatly affected by benchmark datasets and challenges used to standardise the evaluation across geographic regions and weather. The RDD2020 repository provides a collection annotated from smartphones for cracks and potholes, which is the foundation of the Global Road Damage Detection Challenge \cite{rdd2020_2021,grddc2020}. The resulting \gls{rdd2022} extension includes more countries and categories of defects and thereby allows for a more general assessment and encourages benchmarking exercises across countries \cite{rdd2022}. The SVRDD dataset presents street-view imagery as an important new data source that broadens the scope and represents the usefulness of publicly available mapping imagery \cite{svrrd_2024}. Such datasets show practical issues where e.g.~class imbalance, heterogeneous capture viewpoints, and inconsistent illumination are present, all of which directly affect model generalisation. Dataset-centric investigations highlight the importance of categorical labelling protocols and definition of classes in order to help ensure reproducibility. The challenge framework further encourages open comparison between methodologies, which reduces the overfitting to single-region data \cite{grddc2020}. This thesis uses \gls{rdd2022} in order to stay aligned with current benchmark practices but keep the scope manageable in terms of on-device deployment such that the foundation ensures that evaluations in the following chapters can be compared with recent work \cite{yu2024}.

Method-oriented research uses modern detectors and improvements that apply specifically to the problem of road-damage imagery. A \gls{yolo}v7-based strategy with coordinate attention and label smoothing reported significant performance on CRDDC2022, illustrating the advantages of attention mechanisms applied to fine-grained damage pattern recognition \cite{pham2022_yolov7}. An optimised \gls{yolo}v5s for pavement distress identification shows that lightweight modifications of the architecture can significantly boost performance without increasing inference costs \cite{yolov5s_2022}. \gls{gan}-based augmentation approaches have been used in order to augment road damage datasets and increase robustness to low amounts of samples \cite{maeda_gan_2021}. Transformer-based crack detection demonstrates the capacity of attention-driven models to detect long-range structural patterns in pavement defects \cite{guo2023_pavement_transformer}. Benchmark datasets such as the Pavement Image Datasets are available for the evaluation of supplementary contexts for distress classification and detection \cite{majidifard2020_dataset}. These studies agree with the thesis decision to use a \gls{yolo}-based detector, while keeping in mind that data augmentation and attention mechanisms are still key areas to develop in the future. They further prove that improvements of models often depend on better training data than architecture \cite{maeda_gan_2021}. The associated work therefore serves as motivation for the methodological choices used in the proposed on-device system.
