% Phase 4: Chapter 5 - Methods - LaTeX Ready Version


\chapter{Methods\label{cha:chapter5}}

\section{Research methods\label{sec:research_methods}}

The current paper will use a design-and-evaluate approach to research that will connect model development and mobile implementation and field-oriented reporting. First, a small object detector is chosen to meet real-time requirements and maintain a high accuracy to localise defects \cite{yolov8,edgeml2021,terven2023}. Second, the model is trained and tested on a standardised dataset so that it is reproducibly evaluated on defect classes and in visual conditions \cite{rdd2022}. Third, the trained model is translated into on-device inference and combined with a native mobile application to check the viability in the real world \cite{coreml2023,swiftui2022}. The last stage is the assessment of the system based on detection indicators and feasible usability standards that mirror the municipal reporting processes \cite{zaidi2021,smartcitysurvey2021}. This method directly connects the performance of the algorithm to practical usefulness, and does not consider the accuracy as a goal in itself. It also highlights the end-to-end deployment as one of the core requirements in the design process. As a result, the techniques are structured in a way that they prove both technical efficiency and feasibility. These steps of the procedure form the evidence base on which the answers to the research questions that will be discussed in the following chapters will be based.

\section{Datasets}

The first dataset is the Road Damage Dataset 2022 (\gls{rdd2022}), which is a multinational standard of road defect detection \cite{rdd2022}. The data set will include six types of defects that are longitudinal crack, transverse crack, alligator crack, pothole, white-line blur, and other defect. To train, 19089 images are used, and 3579 images are used in validation as per the conventional split that is indicated in the dataset description \cite{rdd2022}. \gls{rdd2022} will be chosen due to the fact that it provides uniform labels and a wide range of road conditions, thus providing essential factors to evaluate thoroughly. The multi-country composition of the dataset provides the model with a variety of textures, lighting conditions and capture positions that accurately reflect actual inspection environment. The use of a commonly used dataset also enables the comparison with other works on road-damage detection that use the same benchmark \cite{yu2024}. The annotations of datasets include bounding boxes that are consistent with the object-detection model used in this thesis. As a result, the dataset used supports the reproducibility and the applicability to municipal maintenance applications. Lastly, the dataset choice is consistent with the current benchmarking trends in the literature of road-damage \cite{rdd2020_2021,svrrd_2024}.

\section{Data Preprocessing steps (if any)}

The images are inputted and reduced to a fixed resolution that is optimal to run inference in real time but still has enough spatial detail to identify small defects \cite{yolov8}. The detection framework has standard normalisation to stabilise the training and increase the convergence. Data augmentation is also used to enhance resistance to lighting changes, perspective changes, and background noise typical of road images \cite{yu2024}. Augmentations include colour jittering and geometric transformations thus allowing the model to be generalised to various road conditions. Mosaic and mix up augmentations are used during the training process to incorporate variations in the samples and reduce over-fitting in a constrained class setting \cite{yolov8}. The augmentation approach is consistent with the modern \gls{yolo} training procedures and emphasises the need to rely on the operational settings \cite{edgeml2021}. The preprocessing is done equally to both training and validation pipelines to maintain consistency in the evaluation. The key preprocessing and augmentation steps used are summarised in Table~\ref{tab:preprocessing-steps} and the augmentation parameters used to train are listed in Table~\ref{tab:augmentation-params}. Figure~\ref{fig:ch5-augmentation-probs} represents the most important augmentation probabilities used in training. All these steps increase the stability of models without providing domain-specific biases that may limit their usage.

\begin{table}[t]
    \centering
    \caption{Preprocessing and augmentation steps used for training.}
    \label{tab:preprocessing-steps}
    \begin{tabular}{p{4.2cm} p{8.8cm}}
        \hline
        Step & Purpose \\
        \hline
        Resize to fixed input & Balance detail with mobile latency. \\
        Normalization & Stabilize training and convergence. \\
        Geometric transforms & Improve viewpoint robustness. \\
        Color jitter & Handle lighting variability. \\
        Mosaic augmentation & Increase sample diversity. \\
        Mixup augmentation & Reduce overfitting in limited classes. \\
        \hline
    \end{tabular}
\end{table}

\begin{table}[t]
    \centering
    \caption{Augmentation parameters used in the training configuration.}
    \label{tab:augmentation-params}
    \begin{tabular}{p{3.6cm} p{2.2cm} p{7.0cm}}
        \hline
        Parameter & Value & Purpose \\
        \hline
        hsv\_h & 0.015 & Hue jitter. \\
        hsv\_s & 0.7 & Saturation jitter. \\
        hsv\_v & 0.4 & Value jitter. \\
        degrees & 10.0 & Rotation degrees. \\
        translate & 0.1 & Translation fraction. \\
        scale & 0.5 & Scaling range. \\
        shear & 2.0 & Shear degrees. \\
        perspective & 0.0 & Perspective transform. \\
        flipud & 0.0 & Vertical flip probability. \\
        fliplr & 0.5 & Horizontal flip probability. \\
        mosaic & 0.9 & Mosaic probability. \\
        mixup & 0.1 & Mixup probability. \\
        copy\_paste & 0.2 & Copy-paste probability. \\
        close\_mosaic & 10 & Disable mosaic after epoch. \\
        \hline
    \end{tabular}
\end{table}

\begin{figure}
    \centering
    \includegraphics[width=0.75\linewidth]{figure_ch5_augmentation.png}
    \caption{Augmentation probabilities used during training.}
    \label{fig:ch5-augmentation-probs}
\end{figure}


\section{Experimental Settings and software used}

Training is performed using the Ultralytics YOLOv8 framework with transfer learning from \gls{coco}-pretrained weights to accelerate convergence \cite{yolov8}. The model is trained for 200 epochs, with a best-performing checkpoint saved at Epoch 119 based on validation metrics, which is standard practice for selecting deployable models \cite{yolov8}. The training pipeline runs on Apple silicon using the Metal Performance Shaders (\gls{mps}) backend for efficient computation, aligning with the target deployment environment. The full training run required approximately 8.8 hours based on the recorded maximum elapsed time in the training log. A fixed input size of 640 pixels is used to balance detection detail and inference speed for mobile use. The \gls{ios} application is developed in \gls{swiftui}, and the trained model is converted to \gls{coreml} for on-device inference \cite{coreml2023,swiftui2022}. Training configuration files and scripts are maintained in the repository to support reproducibility and parameter tracking. Table~\ref{tab:training-hparams} summarises the core training hyperparameters, Table~\ref{tab:software-stack} lists the software environment used for experiments, and Table~\ref{tab:optimization-schedule} details the optimisation schedule used for training. Experimental runs are logged with consistent naming to preserve the link between checkpoints and evaluation summaries. These settings ensure that the experiments are both reproducible and representative of the deployment constraints.

\begin{table}[t]
    \centering
    \caption{Core training hyperparameters used in this thesis.}
    \label{tab:training-hparams}
    \begin{tabular}{p{4.2cm} p{3.0cm} p{6.0cm}}
        \hline
        Parameter & Value & Notes \\
        \hline
        Image size & 640 & Fixed square input for mobile efficiency. \\
        Epochs & 200 & Best checkpoint at Epoch 119. \\
        Batch size & 4 & Tuned for Apple MPS memory limits. \\
        Optimizer & SGD & Ultralytics default for YOLOv8. \\
        Initial learning rate & 0.01 & Standard YOLOv8 setting. \\
        Momentum & 0.937 & Default Ultralytics setting. \\
        Weight decay & 0.0005 & Regularization for stability. \\
        Augmentations & Mosaic, Mixup & Reduced later in training. \\
        \hline
    \end{tabular}
\end{table}

\begin{table}[t]
    \centering
    \caption{Software stack used in training and deployment.}
    \label{tab:software-stack}
    \begin{tabular}{p{4.2cm} p{3.0cm} p{6.0cm}}
        \hline
        Component & Version/Tool & Purpose \\
        \hline
        Training framework & Ultralytics YOLOv8 & Model training and evaluation. \\
        Backend & PyTorch with MPS & Hardware acceleration on macOS. \\
        Conversion & CoreML Tools & Export to iOS runtime format. \\
        Mobile UI & SwiftUI & Native iOS application interface. \\
        \hline
    \end{tabular}
\end{table}

\begin{table}[t]
    \centering
    \caption{Optimization schedule used for training.}
    \label{tab:optimization-schedule}
    \begin{tabular}{p{4.0cm} p{2.6cm} p{6.4cm}}
        \hline
        Parameter & Value & Notes \\
        \hline
        Epochs & 200 & Total training epochs. \\
        Batch size & 4 & MPS-safe batch size. \\
        Initial LR (lr0) & 0.01 & Base learning rate. \\
        Final LR factor (lrf) & 0.01 & Final LR multiplier. \\
        Momentum & 0.937 & Optimizer momentum. \\
        Weight decay & 0.0005 & L2 regularization. \\
        Warmup epochs & 3.0 & Warmup duration. \\
        Warmup momentum & 0.8 & Warmup momentum. \\
        Warmup bias LR & 0.1 & Bias LR during warmup. \\
        Cosine LR schedule & true & Cosine decay enabled. \\
        \hline
    \end{tabular}
\end{table}


\section{Hyperparameter tuning protocol}

\subsection{Search space}
No automated hyperparameter search was performed. The configuration is fixed and follows the Ultralytics YOLOv8 framework defaults with mobile-oriented adjustments. The effective search space is therefore a singleton: learning rate (0.01), batch size (4), epochs (200), input resolution (640), optimizer (SGD), and augmentation parameters as listed in Table~\ref{tab:augmentation-params}. These values were chosen to align with documented YOLOv8 practices and \gls{mps} memory limits rather than through iterative search \cite{yolov8}.

\subsection{Budget}
The hyperparameter search budget is zero trials. A single training run was executed with the fixed configuration described above. No grid search, random search, or Bayesian optimisation was applied.

\subsection{Validation-only tuning and no test leakage}
All tuning and model selection use only training and validation data. The best checkpoint is selected solely on validation \gls{map} and related metrics during training; no separate test set exists or is used for selection. Validation data is used exclusively for checkpoint selection and performance reporting. No test split is used for tuning, and no test data is involved in any model or hyperparameter decision. This protocol avoids test leakage and keeps the evaluation unbiased.

\section{Network Architecture (for deep learning models only)}

The detection model in this thesis is built on the basis of \gls{yolov8s}, which is a single-stage architecture optimised towards real-time performance and with a small number of parameters \cite{yolov8}. The model uses a backbone to extract features, a neck to combine multi-scale features, and a detection head to produce bounding boxes and class probabilities. This design enables predictions of small and elongated road defects at scale, which is essential in detecting small and elongated defects on the road \cite{yolov8,yu2024}. The reason behind selecting \gls{yolov8s} is that it provides a trade-off between performance and mobile compatibility which does not need the computational cost of larger models \cite{edgeml2021}. It has a trained model with a size of about 11.14 million parameters and is packaged to be used on \gls{ios} devices after conversion to \gls{coreml} \cite{coreml2023}. The architecture enables anchor-free prediction as well as modern training optimisations that help to minimise the post-processing overhead. This architecture meets the requirement of the thesis of real-time on-device inference and maintains reasonable detection accuracy. Table~\ref{tab:model-summary} summarises the important architectural properties used in this thesis. As a result, the architecture is the main technical element of the designed system.


\begin{table}[t]
    \centering
    \caption{Model summary for the YOLOv8s configuration used in this thesis.}
    \label{tab:model-summary}
    \begin{tabular}{p{4.2cm} p{8.8cm}}
        \hline
        Item & Value \\
        \hline
        Architecture & YOLOv8s \\
        Parameters & 11.14M \\
        Model size & 21.50 MB \\
        Input size & 640 \\
        Backbone/neck/head & Backbone, neck, detection head \\
        \hline
    \end{tabular}
\end{table}


\section{Mobile Application Design and Workflow}

The trained detector is realised as the \gls{ios} application, an all-encompassing on-device reporting tool; the application is developed in \gls{swiftui} and is based on a \gls{coreml} model that performs the real-time inference step, a local persistence framework that stores detection history, and device services for camera and geolocation \cite{swiftui2022,coreml2023}. The architecture is deliberately sparse to represent a bare-bone field workflow: image capture or selection, inference, detection review, and report generation. The user interface is divided into four modules, each with a matching data model, and the resulting detections flow through the infrastructure. Focussing on quick completion of tasks rather than full elaboration keeps the design aligned with municipal inspection practice and ensures that non-technical personnel in the field can use it without extensive training; the interaction sequence also has a close relationship with the evaluation objectives presented in the following chapters.

The capture module supports both live camera inference and photo library analysis, thus supporting real-time and offline use cases. In live camera mode, frames are sent to the \gls{coreml} model at a fixed input resolution, and each frame is preprocessed in the application domain to comply with the input resolution and normalisation standards used at the time of model export. In photo library mode, batch inspection of pictures accumulated in the mobile application is allowed, which is especially useful in case of low bandwidth or time constraints that would prevent immediate review of a captured image. The inference module executes the \gls{yolov8s} \gls{coreml} model and applies \gls{nms} to remove overlapping predictions. The final detections contain class labels, confidence scores, and bounding boxes and are shown as overlays on the image; a brief legend is displayed to ensure that onsite inspection maintains visibility of the defect regions whilst providing class information at the same time, thus facilitating rapid decision making in the field and prioritising clarity and speed rather than dense hyper-analytics.

Each detection event is stored locally together with its timestamp, predicted classes, confidence values, and the associated image. \gls{gps} coordinates are captured at the time of detection using the device's location service and stored concurrently to support geo-referenced reporting. The history module displays detections in a chronological list and allows users to review information, including per-class counts and the original image with overlays, thus creating a local audit trail and reducing the need for manual note taking during inspections. The reporting module transforms a selected detection into a structured report that consolidates classes, location, time, and the annotated image into a single summary view. The application provides a curated list of municipal authority contacts in many countries, enabling the user to pick the right contact depending on location. Reports can be shared via standard \gls{ios} actions including email or message, thus connecting technical inference to operational reporting in a traceable and repeatable way.

\section{Other details for reproducing your methodology or results}

Reproducibility is guaranteed by saving the scripts and configuration files that spell out the paths of datasets, training settings, and augmentation settings. The training script takes configuration overrides to ensure that experiments can be repeated under controlled variations. Training saves checkpoints, and the best-performing checkpoint in terms of validation is then chosen and used in deployment. Summary evaluations of models are also stored with the training results in order to maintain metric provenance. Export to \gls{coreml} is based on the standard export pipeline supported by the Ultralytics framework and \gls{ios} tools \cite{coreml2023}. The mobile application combines end-to-end validation of the pipeline through the use of a consistent data model with inference, \gls{gps} tagging, and reporting capabilities \cite{swiftui2022}. Repository documentation describes the implementation of the model into the \gls{ios} app as well as how to recreate the training. The supporting materials and implementation are stored in an open repository to ensure reproducibility and extensibility in the future \cite{cardaozel2026}. Documentation of the methodology is necessary to ensure that it can be reproduced in various hardware settings \cite{edgeml2021}. These measures ensure that the results can be reproduced and verified without undocumented assumptions.

\section{Techniques for Data Analysis/Visualization}

The convergence dynamics were studied using training logs, and the epoch with the best validation performance was identified. Performance measures were condensed into tables and graphs to illustrate precision, recall, and mean average precision (\gls{map}) curves during the course of training. To identify misalignment between predicted bounding boxes and defect regions, visual inspection of detection outputs was performed with the help of exemplar images. The use of confusion matrices and precision--recall curves was also extended in the following chapters to clarify class-specific performance and threshold trade-offs \cite{zaidi2021}. In the context of the mobile application, qualitative screenshots were used for real-time inference, detection overlays, and reporting flows. Figures~\ref{fig:training-curves}, \ref{fig:pr-curve} and \ref{fig:confusion-matrix} illustrate the standard visual output used to interrogate model behaviour. These illustrations provide indications of practical applicability, thus supporting quantitative indicators. In addition, they allow the analysis of errors by determining which classes or thresholds are most significant for missed detections. Raw data tables were provided to support all figures, as required by the documentation. Taken together, these analytical methods provide a balanced view of model stability, accuracy, and field readiness.


\begin{figure}
    \centering
    \includegraphics[width=1\linewidth]{results.png}
    \caption{Training curves showing loss, precision, recall, and \gls{map} across epochs.}
    \label{fig:training-curves}
\end{figure}

\begin{figure}
    \centering
    \includegraphics[width=0.9\linewidth]{BoxPR_curve.png}
    \caption{Precision--recall curve for the validation set.}
    \label{fig:pr-curve}
\end{figure}

\begin{figure}
    \centering
    \includegraphics[width=0.9\linewidth]{confusion_matrix.png}
    \caption{Confusion matrix for the six defect classes in \gls{rdd2022}.}
    \label{fig:confusion-matrix}
\end{figure}


\section{Evaluation Metrics}

The performance of the model is evaluated based on standard object-detection metrics, including precision, recall, and mean Average Precision (\gls{map}) at various Intersection-over-Union (\gls{iou}) thresholds \cite{zaidi2021}. The \gls{map}@0.5 value provides a baseline metric of detection accuracy, and \gls{map}@0.5:0.95 ensures a higher quality of localisation \cite{zaidi2021}. These metrics are reported alongside model size and parameter count to emphasise the trade-off between accuracy and deployment feasibility \cite{edgeml2021}. Inference latency and real-time throughput are considered as operational metrics in the context of mobile deployment, as they define usability in the field environment \cite{coreml2023}. Validation results are summarised to identify the best checkpoint for deployment, which is consistent with standard model-selection practice \cite{yolov8}. The metrics and their interpretation are outlined in Table~\ref{tab:metric-definitions}. The calculations are performed on the validation split of \gls{rdd2022} to ensure comparability with prior research \cite{rdd2022}. The evaluation framework therefore aligns accuracy, efficiency, and practical constraints. These metrics directly support the answers to the research questions formulated in Chapter~\ref{cha:chapter4} and allow direct comparison with current road-damage benchmarks \cite{rdd2022,svrrd_2024}.

\begin{table}[t]
    \centering
    \caption{Evaluation metrics used in this thesis.}
    \label{tab:metric-definitions}
    \begin{tabular}{p{3.8cm} p{9.4cm}}
        \hline
        Metric & Definition and use \\
        \hline
        Precision & Proportion of predicted defects that are correct. \\
        Recall & Proportion of ground-truth defects that are detected. \\
        \gls{map}@0.5 & Average precision at \gls{iou} threshold 0.5. \\
        \gls{map}@0.5:0.95 & Average precision across \gls{iou} thresholds 0.5--0.95. \\
        Latency & Time per inference on mobile hardware. \\
        \hline
    \end{tabular}
\end{table}
