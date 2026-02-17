% Phase 4: Chapter 6 - Experiments and Results - LaTeX Ready Version
% Copy the content below into your Overleaf Chapter 6 section

\chapter{Experiments and results\label{cha:chapter6}}

\section{Model Training\label{sec:training}}

\subsection{Environment}

Training and evaluation were done on macOS using \gls{mps} in order to match the development environment to the target \gls{ios} deployment stack \cite{coreml2023}. The YOLOv8 framework provided the training loop, logging, and validation pipeline that was used for all experiments \cite{yolov8}. A uniform input size of 640 pixels was used to trade off detail and throughput for real-time inference \cite{yolov8}. Training was done for 200 epochs with a small batch size so as not to encounter memory pressure on \gls{mps} whilst keeping convergence stable. The exported evaluation configuration produced a model of 21.50 MB with 11.14M parameters, which is suitable for mobile deployment constraints \cite{edgeml2021}. Table~\ref{tab:training-env} summarises the environment and core settings for reproducibility, and Table~\ref{tab:checkpoint-summary} gives a brief summary of the overall run. These settings provide a realistic approximation of mobile inference constraints whilst ensuring reproducibility \cite{edgeml2021}. The environment choices directly reflect the thesis goal of on-device deployment rather than server-centric training.

\subsection{Training process}

The model was trained for 200 epochs using transfer learning from \gls{coco}-pretrained weights to speed up convergence and improve stability \cite{yolov8}. The training log records a maximum elapsed time of 31,571 seconds for the full run, which corresponds to roughly 8.8 hours on the \gls{mps} backend. Several attempts to enhance accuracy were made during this single run through strong augmentation, a longer schedule, and careful checkpoint selection \cite{edgeml2021}. The checkpoint with the highest validation performance was selected at Epoch 119, which is standard practice for deployment selection \cite{yolov8}. During training, validation was carried out to track precision, recall, and \gls{map} trends, enabling early detection of overfitting or degradation \cite{zaidi2021}. Figure~\ref{fig:training-curves} shows the training curves used to select the checkpoint and verify convergence behaviour. The best checkpoint achieved \gls{map}@0.5 of 49.19\% with precision of 60.43\%, and this model was used for the \gls{ios} deployment as documented in Phase 4 model selection notes. Although the last epoch is reported for completeness, deployment prioritises the best validation checkpoint for accuracy stability. Table~\ref{tab:checkpoint-summary} summarises the best and final checkpoint metrics, and Figure~\ref{fig:pr-curve} illustrates the precision--recall comparison for quick interpretation. This training procedure ensures that the deployed model represents the strongest validated performance rather than the last epoch.

\section{Experiments\label{sec:experiments}}

\subsection{Quantitative Evaluation}

The main experiment determines the detection accuracy on the \gls{rdd2022} validation split using standard object detection metrics \cite{rdd2022,zaidi2021}. The best checkpoint achieves mean Average Precision at \gls{iou} threshold 0.5 of 0.4919 and mean Average Precision over \gls{iou} thresholds 0.5:0.95 of 0.2058, with precision 0.6043 and recall 0.4722. These values represent the trade-off between accuracy and coverage across the six defect classes. Figure~\ref{fig:pr-curve} shows the precision--recall curve, which facilitates analysis of threshold trade-offs. Figure~\ref{fig:confusion-matrix} shows the confusion matrix, which highlights class-level confusions and allows qualitative interpretation of errors. The evaluation summary is presented in Table~\ref{tab:eval-summary}, which provides a summary of the major metrics for rapid evaluation. The metrics are computed on the validation split to maintain comparability with prior \gls{rdd2022} investigations \cite{rdd2022,rdd2020_2021}. This experiment sets the baseline performance needed to answer RQ1 on detection accuracy.

\subsection{Qualitative Detections}

The second experiment evaluates qualitative detection behaviour by examining predicted bounding boxes on validation images \cite{rdd2022}. The example outputs validate that defects of various shapes and sizes are detected consistently, which is especially important for small cracks and elongated damage patterns \cite{yu2024}. Figure~\ref{fig:val-detections} shows representative predictions produced by the trained model. These examples are used to confirm that detections align with visible defect regions and that confidence scores reflect the expected uncertainty. The qualitative analysis complements metric-based evaluation by identifying errors that may not be evident from aggregated scores. It also meets the usability requirement by demonstrating clear visualisation of detections for field workers. Visual clarity and interpretability are key elements of effective municipal reporting. In addition, the qualitative inspection serves to validate that the model outputs have practical value for reporting workflows. Together with the quantitative metrics, these examples provide compelling evidence that the model is suitable for on-device deployment.

\section{Model Generalization}

Generalization is analysed in terms of performance stability across diverse road conditions and defect classes present in \gls{rdd2022} \cite{rdd2022}. The dataset includes various countries and capture conditions, which provides a reasonable proxy for real-world variability \cite{rdd2022,yu2024}. The observed precision and recall values indicate that the model maintains consistent detection quality across the validation split. Class imbalance and small-object sensitivity remain challenges, as reflected by lower recall compared to precision. The confusion matrix outlines where visually similar defects may be misclassified, which informs potential future improvements in data augmentation or class weighting. Despite these challenges, the model achieves credible detection across the six categories, supporting the feasibility of deployment. Qualitative detections also suggest that the model generalises to diverse textures and lighting conditions. The best checkpoint \gls{map}@0.5 of 49.19\% indicates a practical accuracy ceiling under the current mobile constraints, and higher accuracy would likely require larger models or additional data \cite{edgeml2021}. This section therefore provides substantial support for RQ1 and RQ2 by showing that accuracy is not limited to a restricted subset of the data.

\section{Comparison with Existing Techniques}

The comparison to prior work highlights the trade-off between detection accuracy and mobile feasibility rather than absolute accuracy alone \cite{edgeml2021,terven2023}. Large detectors can achieve higher \gls{map} but often exceed mobile resource constraints, which limits practical use in field workflows. The chosen \gls{yolov8s} model has a compact footprint but provides competitive accuracy for mobile deployment, aligning with recent trends in efficient detectors \cite{yolov8,yolov7_2022}. Road damage studies using YOLO variants emphasize the importance of lightweight architectures and robust training pipelines for real-world conditions \cite{pham2022_yolov7,yolov5s_2022}. Table~\ref{tab:comparison-notes} summarises qualitative comparisons with representative techniques from the literature, focusing on deployment suitability. This discussion supports the thesis decision to prioritise on-device feasibility whilst maintaining acceptable detection performance. The results therefore position the proposed system as a viable alternative to heavier models that are difficult to deploy on mobile devices. The comparison also indicates that mobile feasibility is the major distinguishing factor between modern detectors. This section contributes to answering RQ2 by aligning the model choice with deployment constraints.

Figures~\ref{fig:training-curves}--\ref{fig:val-detections} present the quantitative and qualitative evidence discussed in this chapter, including training dynamics, precision--recall behaviour, confusion trends, and example detections.

\begin{figure}[t]
    \centering
    \includegraphics[width=0.95\linewidth]{figures/results.png}
    \caption{Training curves showing loss, precision, recall, and \gls{map} across epochs.}
    \label{fig:training-curves}
\end{figure}

\begin{figure}[t]
    \centering
    \includegraphics[width=0.80\linewidth]{figures/BoxPR_curve.png}
    \caption{Precision--recall curve for the validation set.}
    \label{fig:pr-curve}
\end{figure}

\begin{figure}[t]
    \centering
    \includegraphics[width=0.75\linewidth]{figures/confusion_matrix.png}
    \caption{Confusion matrix for the six defect classes in \gls{rdd2022}.}
    \label{fig:confusion-matrix}
\end{figure}

\begin{figure}[t]
    \centering
    \includegraphics[width=0.95\linewidth]{figures/val_batch2_pred.jpg}
    \caption{Representative detection outputs on the validation set.}
    \label{fig:val-detections}
\end{figure}

\begin{table}[t]
    \centering
    \caption{Training environment and core settings.}
    \label{tab:training-env}
    \begin{tabular}{p{4.0cm} p{8.8cm}}
        \hline
        Item & Setting \\
        \hline
        Framework & Ultralytics YOLOv8 (PyTorch with \gls{mps}) \\
        Input size & 640 \\
        Epochs & 200 \\
        Batch size & 4 \\
        Device & Apple \gls{mps} backend \\
        \hline
    \end{tabular}
\end{table}

\begin{table}[t]
    \centering
    \caption{Checkpoint summary used for reporting and deployment.}
    \label{tab:checkpoint-summary}
    \begin{tabular}{p{3.0cm} p{2.0cm} p{2.2cm} p{2.2cm} p{2.2cm}}
        \hline
        Checkpoint & Epoch & \gls{map}@0.5 & Precision & Recall \\
        \hline
        best.pt & 119 & 49.19\% & 60.43\% & 47.22\% \\
        last.pt & 200 & 42.03\% & 48.69\% & 41.15\% \\
        \hline
    \end{tabular}
\end{table}

\begin{table}[t]
    \centering
    \caption{Evaluation summary on the validation split.}
    \label{tab:eval-summary}
    \begin{tabular}{p{4.0cm} p{3.0cm}}
        \hline
        Metric & Value \\
        \hline
        \gls{map}@0.5 & 0.4919 \\
        \gls{map}@0.5:0.95 & 0.2058 \\
        Precision & 0.6043 \\
        Recall & 0.4722 \\
        \gls{f1} score & 0.5302 \\
        Balanced accuracy & 0.4722 \\
        Model size & 21.50 MB \\
        Parameters & 11.14M \\
        \hline
    \end{tabular}
\end{table}

\begin{table}[t]
    \centering
    \caption{Qualitative comparison with representative techniques.}
    \label{tab:comparison-notes}
    \begin{tabular}{p{3.6cm} p{3.0cm} p{5.4cm}}
        \hline
        Technique & Focus & Deployment suitability \\
        \hline
        \gls{yolov8s} (this work) & Real-time, compact & Designed for mobile inference and \gls{coreml} export. \\
        YOLOv7 variants & High accuracy & Strong real-time performance but heavier models. \\
        PP-YOLOE & Industrial speed & Efficient but less common in \gls{ios} pipelines. \\
        RT-DETR & Transformer-based & Competitive accuracy, higher compute cost. \\
        \hline
    \end{tabular}
\end{table}
